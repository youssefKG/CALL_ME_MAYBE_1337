from models import functions_call
from src.models.function_definition_model import (
    FunctionDefinitionModel,
)
from src.models.prompt_model import PromptModel
from src.models.functions_call import FunctionCall, FunctionsCall
from pathlib import Path


class ErrorRecovery:
    def __init__(
        self,
        output_path: str,
        function_definitions: list[FunctionDefinitionModel],
        prompts: list[PromptModel],
    ) -> None:
        self.__output_path: str = output_path
        self.__functions_definitions: list[FunctionDefinitionModel] = (
            function_definitions
        )
        self.__prompts: list[str] = [prompt.prompt for prompt in prompts]
        self.__generated_functions_call: list[FunctionCall]
        self.__generated_prompts: list[str] = list()
        self.__remaining_prompts: list[str] = list()

    def recover(self) -> None:
        function_defintion: FunctionDefinitionModel | None
        self.__set_generated_functions_call()
        for function_call in self.__generated_functions_call:
            function_defintion = self.__get_function_definition_from_function_call(
                function_call.name
            )
            if function_defintion is None:
                self.__generated_functions_call = list()
                self.__generated_prompts = self.__prompts
                break

    def __set_generated_functions_call(self) -> None:
        functions_call_content: str = Path(self.__output_path).read_text()
        self.__generated_functions_defitions = FunctionsCall.model_validate_json(
            functions_call_content
        ).root
        for prompt, function_call in zip(
            self.__prompts, self.__generated_functions_call
        ):
            if prompt != function_call.prompt:
                pass

    def __get_function_definition_from_function_call(
        self, function_call_name: str
    ) -> FunctionDefinitionModel | None:
        for function_definition in self.__functions_definitions:
            if function_definition.name == function_call_name:
                return function_definition
        else:
            return None

    def __set_default(self) -> None:
        self.__generated_functions_call = list()
