from pydantic import ValidationError

from src.log.log import Log, LogRow
from src.models.function_definition_model import (
    FunctionDefinitionModel,
)
from src.models.prompt_model import PromptModel
from src.models import FunctionCallModel, FunctionCallRootModel
from pathlib import Path


class ErrorRecovery:
    def __init__(
        self,
        *,
        log: Log,
        output_path: str,
        function_definitions: list[FunctionDefinitionModel],
        prompts: list[PromptModel],
    ) -> None:
        self.__output_path: str = output_path
        self.__functions_definitions: list[FunctionDefinitionModel] = (
            function_definitions
        )
        self.__prompts: list[PromptModel] = prompts
        self.__generated_functions_call: list[FunctionCallModel] = list()
        self.__generated_prompts: list[str] = list()
        self.__remaining_prompts: list[PromptModel] = list()
        self.__log: Log = log
        self.__init_log()

    def recover(self) -> None:
        function_defintion: FunctionDefinitionModel | None = None
        try:
            self.__set_generated_functions_call()
        except ValidationError:
            self.__set_default()
            return
        idx: int = 0
        if len(self.__prompts) < len(self.__generated_functions_call):
            self.__set_default()
            return
        for prompt, function_call in zip(
            self.__prompts, self.__generated_functions_call
        ):
            function_defintion = self.__get_function_definition_from_function_call(
                function_call.name
            )
            if any(
                [
                    prompt.prompt != function_call.prompt,
                    function_defintion is None
                    or not self.__is_valid_arguments(function_call, function_defintion),
                ]
            ):
                self.__set_default()
                idx = 0
                break
            idx += 1
        if idx != 0:
            self.__log_generated_function_calls()
        self.__remaining_prompts = self.__prompts[idx:]

    def __set_generated_functions_call(self) -> None:
        functions_call_content: str = Path(self.__output_path).read_text()
        self.__generated_functions_call = FunctionCallRootModel.model_validate_json(
            functions_call_content
        ).root

    def __get_function_definition_from_function_call(
        self, function_call_name: str
    ) -> FunctionDefinitionModel | None:
        for function_definition in self.__functions_definitions:
            if function_definition.name == function_call_name:
                return function_definition
        else:
            return None

    def __is_valid_arguments(
        self,
        function_call: FunctionCallModel,
        function_definition: FunctionDefinitionModel | None,
    ) -> bool:
        if function_definition:
            for arg_name, arg_type in function_definition.parameters.items():
                if arg_name not in function_call.parameters.keys():
                    return False
                match arg_type.type:
                    case "string":
                        if not isinstance(function_call.parameters[arg_name], str):
                            return False
                    case "integer":
                        if not isinstance(function_call.parameters[arg_name], int):
                            return False
                    case "boolean":
                        if not isinstance(function_call.parameters[arg_name], bool):
                            return False
                    case "number":
                        if not isinstance(function_call.parameters[arg_name], float):
                            return False
                    case "float":
                        if not isinstance(function_call.parameters[arg_name], float):
                            return False
        return True

    def __set_default(self) -> None:
        self.__generated_functions_call = list()
        self.__remaining_prompts = self.__prompts

    @property
    def remaining_prompts(self) -> list[PromptModel]:
        return self.__remaining_prompts

    @property
    def generated_functions_calls(self) -> list[FunctionCallModel]:
        return self.__generated_functions_call

    def __init_log(self) -> None:
        self.__log.add_rows(
            [LogRow(prompt.id, prompt.prompt) for prompt in self.__prompts]
        )

    def __log_generated_function_calls(self) -> None:
        for prompt, function_call in zip(
            self.__prompts, self.__generated_functions_call
        ):
            function_definition: FunctionDefinitionModel | None = (
                self.__get_function_definition_from_function_call(function_call.name)
            )
            if function_definition:
                self.__log.add_row(
                    LogRow(
                        prompt.id,
                        prompt.prompt,
                        function_definition.model_dump_json(indent=4),
                        function_call.model_dump_json(indent=4),
                    )
                )
