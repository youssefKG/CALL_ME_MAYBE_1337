from src.predictors.fn_name_predictor import FnNamePredictor
from src.LlmModel.model import Model
from src.Parser.Parser import Parser
from src.prompts.prompt_generator import PromptGenerator
from src.cache.cache import Cache
import torch


class Generator:
    def __init__(self, parser: Parser) -> None:
        self.__model: Model = Model()
        self.__cache = Cache()
        self.__parser: Parser = parser
        print("===============================")
        print("functions" ,self.__parser.get_fns_def)
        self.__prompt_generator: PromptGenerator = (
            PromptGenerator.Builder(
                self.__parser.get_fns_def, self.__parser.get_prompts
            )
            .set_params_static_prompt()
            .set_fns_def_static_prompt()
            .build()
        )
        self.__fn_predictor: FnNamePredictor = FnNamePredictor()
        self.__init_cache()
        self.__init_fns_def_predictor()
        self.__fn_predictor.get_next_predictions_ids([])

    def generate_prompt_ids(self, prompt: str) -> callable:
        text_ids: list[int] = list()
        fns_def_dynamic_prompt: str = (
            self.__prompt_generator.get_fns_def_dynamic_prompt(prompt)
        )
        fns_def_dynamic_prompt_ids: list[int] = self.__model.encode_text(
            fns_def_dynamic_prompt
        )
        fns_static_prompts_ids: list[int] = self.__cache.get_params_ids
        text_ids += fns_def_dynamic_prompt_ids + fns_static_prompts_ids
        print(self.__prompt_generator.get_fns_def_static_prompt, end="")
        print(fns_def_dynamic_prompt, end="")

        def generate(token_id: int | None = None) -> list[int]:
            nonlocal text_ids
            if token_id is None:
                return text_ids
            text_ids.append(token_id)
            return text_ids

        return generate

    def get_next_token(self, text_ids: list[int]) -> tuple[str, int]:
        logits: list[float] = self.__model.get_logits(text_ids)
        props_ids = torch.argmax(torch.tensor(logits), dim=-1).item()
        token: str = self.__model.decode(torch.tensor(props_ids))
        token_id: int = self.__model.encode_text(token)[0]
        return (token, token_id)

    @property
    def next_prompt(self) -> str:
        return next(self.__prompt_generator.next_prompt)

    def __set_fns_names_to_predictors(self) -> None:
        pass

    def __init_cache(self) -> None:
        encoded_fns_def_names_ids: list[int] = self.__model.encode_text(
            self.__prompt_generator.get_fn_params_static_prompt
        )
        encoded_fn_def_params_ids: list[int] = self.__model.encode_text(
            self.__prompt_generator.get_fns_def_static_prompt
        )
        self.__cache.set_fns_def_static_prompt_ids(encoded_fns_def_names_ids)
        self.__cache.set_fn_params_static_prompt_ids(encoded_fn_def_params_ids)

    def __init_fns_def_predictor(self) ->  None:
        fns_def_names_ids: list[list[int]] = list()
        for fn_def in self.__parser.get_fns_def:
            fns_def_names_ids.append(self.__model.encode(fn_def["name"]))
        self.__fn_predictor.add(fns_def_names_ids)
