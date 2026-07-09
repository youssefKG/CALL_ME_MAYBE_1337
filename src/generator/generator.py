from collections.abc import Generator
from src.predictors.fn_name_predictor import FnNamePredictor
from src.LlmModel.model import Model
from src.Parser.Parser import Parser
from src.prompts.prompt_generator import PromptGenerator
from src.cache.cache import Cache
import torch


class FunctionNameGenerator:
    def __init__(
        self,
        model: Model,
        cache: Cache,
        fn_predicor: FnNamePredictor,
        prompt_generator: PromptGenerator,
        prompt: str,
    ) -> None:
        self.__model = model
        self.__prompt_generator: PromptGenerator = prompt_generator
        self.__function_name_predictor: FnNamePredictor = fn_predicor
        self.__cache: Cache = cache
        self.__text_ids: list[int] = list()
        self.__generated_ids: list[int] = list()
        self.__fn_name_list: list[str] = list()
        self.__prompt: str = prompt
        self.__fn_name: str = ""
        self.__init_text_ids()

    def generate(self) -> None:
        while True:
            self.__predict_next_token()
            if self.__function_name_predictor.is_completed(self.__generated_ids):
                break
            predicted_ids: list[int] = (
                self.__function_name_predictor.get_next_predictions_ids(
                    self.__generated_ids
                )
            )
            logits: list[float] = self.__model.get_logits(self.__text_ids)
            for idx, _ in enumerate(logits):
                if idx not in predicted_ids:
                    logits[idx] = float("-inf")
            high_score = torch.argmax(torch.tensor(logits))
            self.__add_next_token_id(int(high_score))
        self.__fn_name = "".join(self.__fn_name_list)

    def __add_next_token_id(self, id: int) -> None:
        self.__generated_ids.append(id)
        self.__text_ids.append(id)
        token: str = self.__model.decode(torch.tensor(id))
        self.__fn_name_list.append(token)

    def __init_text_ids(self) -> None:
        self.__text_ids = (
            self.__cache.get_function_name_static_prompt_ids
            + self.__model.encode_text(
                self.__prompt_generator.get_fns_def_dynamic_prompt(self.__prompt)
            )
        )

    def __predict_next_token(self) -> None:
        next_predicted_ids: list[int] = (
            self.__function_name_predictor.get_next_predictions_ids(
                self.__generated_ids
            )
        )
        while len(next_predicted_ids) == 1:
            next_token_id: int = next_predicted_ids[0]
            self.__text_ids.append(next_token_id)
            self.__generated_ids.append(next_token_id)
            next_token: str = self.__model.decode(torch.tensor(next_token_id))
            self.__fn_name_list.append(next_token)
            next_predicted_ids = (
                self.__function_name_predictor.get_next_predictions_ids(
                    self.__generated_ids
                )
            )

    @property
    def fn_name(self) -> str:
        return self.__fn_name

    def __mask_low_score_logits(
        self, logits: list[float], high_score_ids: list[int]
    ) -> None:
        for idx, _ in enumerate(logits):
            if idx not in high_score_ids:
                logits[idx] = float("-inf")


class FunctionParametreGenerator:
    def __init__(
        self,
        static_prompt_ids: list[int],
        prompt_generator: PromptGenerator,
        model: Model,
    ) -> None:
        self.prompt_generator: PromptGenerator = prompt_generator
        self.generated_ids: list[int] = list()
        self.__text_ids: list[int] = list()
        self.__model: Model = model
        self.__set_static_parametre_ids()

    def generate(self) -> None:
        while True:
            pass

    def __set_static_parametre_ids(self) -> None:
        pass


class OutputGenerator:
    def __init__(self, parser: Parser) -> None:
        self.__model: Model = Model()
        self.__cache = Cache()
        self.__parser: Parser = parser
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

    def generate(self) -> Generator[str | None]:
        yield ""

    def generate_function_name(self) -> Generator[str | None]:
        prompt_generator: Generator[str | None] = self.__prompt_generator.next_prompt
        prompt: str | None = next(prompt_generator)
        while prompt is not None:
            print(prompt)
            fn_name_generator: FunctionNameGenerator = FunctionNameGenerator(
                self.__model,
                self.__cache,
                self.__fn_predictor,
                self.__prompt_generator,
                prompt,
            )
            fn_name_generator.generate()
            yield fn_name_generator.fn_name
            prompt = next(prompt_generator)
        yield None

    def __init_cache(self) -> None:
        encoded_fns_def_names_ids: list[int] = self.__model.encode_text(
            self.__prompt_generator.get_fn_params_static_prompt
        )
        encoded_fn_def_params_ids: list[int] = self.__model.encode_text(
            self.__prompt_generator.get_fns_def_static_prompt
        )
        self.__cache.set_fns_def_static_prompt_ids(encoded_fns_def_names_ids)
        self.__cache.set_fn_params_static_prompt_ids(encoded_fn_def_params_ids)

    def __init_fns_def_predictor(self) -> None:
        fns_def_names_ids: list[list[int]] = list()
        for fn_def in self.__parser.get_fns_def:
            fns_def_names_ids.append(self.__model.encode_text(fn_def.name))
        self.__fn_predictor.set_fns_names_ids_trie(fns_def_names_ids)
