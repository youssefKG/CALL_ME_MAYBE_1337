from src.predictors.fn_name_predictor import FunctionNamePredictor
from src.LlmModel.model import Model
from src.prompts.prompt_generator import PromptGenerator
from src.cache.cache import Cache
import torch


class FunctionNameGenerator:
    def __init__(
        self,
        model: Model,
        cache: Cache,
        fn_predicor: FunctionNamePredictor,
        prompt_generator: PromptGenerator,
        prompt: str,
    ) -> None:
        self.__model = model
        self.__prompt_generator: PromptGenerator = prompt_generator
        self.__function_name_predictor: FunctionNamePredictor = fn_predicor
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
            logits: list[float] = self.__model.get_masked_logits(
                self.__text_ids, predicted_ids
            )
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
            self.__add_next_token_id(next_token_id)
            next_predicted_ids = (
                self.__function_name_predictor.get_next_predictions_ids(
                    self.__generated_ids
                )
            )

    @property
    def fn_name(self) -> str:
        return self.__fn_name
