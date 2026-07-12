from src.models.function_definition_model import FunctionDefinitionModel
from src.predictors.fn_param_predictor import FunctionParamsPredicor
from src.LlmModel.model import Model
from src.cache.cache import Cache
from collections.abc import Generator
from src.prompts.prompt_generator import PromptGenerator
import torch
from src.utils.function_parameter import FunctionParameter


class FunctionParametreGenerator:

    def __init__(
        self,
        prompt_generator: PromptGenerator,
        param_predictor: FunctionParamsPredicor,
        user_prompt: str,
        function_definition: FunctionDefinitionModel,
        model: Model,
        cache: Cache,
    ) -> None:

        self.__prompt_generator: PromptGenerator = prompt_generator
        self.__text_ids: list[int] = list()
        self.__model: Model = model
        self.__generated_arguments: list[FunctionParameter] = list()
        self.__user_prompt: str = user_prompt
        self.__function_definition: FunctionDefinitionModel = function_definition
        self.__cache: Cache = cache

    def generate(self) -> None:
        arg_generator: Generator[tuple[str, str] | None] = (
            self.__next_argument_generator()
        )
        argument: tuple[str, str] | None = next(arg_generator)
        while argument:
            arg_name, arg_type = argument
            self.__prepare_next_argument(arg_name, arg_type)
            if arg_type == "number":
                pass
            elif arg_type == "string":
                pass
            else:
                break
            argument = next(arg_generator)

    def __generate_function_argument(self, arg_name: str, arg_value: str) -> None:
        i: int = 0
        while i < 10:
            logits: list[float] = self.__model.get_logits(self.__text_ids)
            hight_score = torch.argmax(torch.tensor(logits))

    def generate_param_number(self) -> int:
        generated_ids: list[int] = list()
        possible_tokens: list[int] = self.__cache.get_numbers_ids
        while True:
            pass

    def __set_dynamic_prompt(self, arg_name: str, arg_value: str) -> None:
        dynamic_prompt: str = (
            self.__prompt_generator.get_function_arguments_dynamic_prompt(
                self.__function_definition,
                self.__user_prompt,
                self.__generated_arguments,
                arg_name,
                arg_value,
            )
        )
        dynamic_prompt_ids: list[int] = self.__model.encode_text(dynamic_prompt)
        self.__text_ids += dynamic_prompt_ids

    def __set_static_prompt_ids(self) -> None:
        self.__text_ids += self.__cache.get_function_argument_static_prompt_ids

    def __next_argument_generator(self) -> Generator[tuple[str, str] | None]:
        for arg_name, arg in self.__function_definition.parameters.items():
            yield (arg_name, arg.type)
        yield None

    def __prepare_next_argument(self, arg_name: str, arg_type: str) -> None:
        self.__set_static_prompt_ids()
        self.__set_dynamic_prompt(arg_name, arg_type)
