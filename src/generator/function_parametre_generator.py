from src.predictors.fn_param_predictor import FunctionParamsPredicor
from src.LlmModel.model import Model
from src.prompts.prompt_generator import PromptGenerator


class FunctionParametreGenerator:
    def __init__(
        self,
        prompt_generator: PromptGenerator,
        param_predictor: FunctionParamsPredicor,
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
