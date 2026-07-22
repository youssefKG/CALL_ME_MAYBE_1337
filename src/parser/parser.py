from pathlib import Path
from src.models.function_definition_model import (
    FunctionsDefinitionRootModel,
    FunctionDefinitionModel,
)
from .ArgParser import ArgsParser
from src.models.prompt_model import PromptModel, PromptsRootModel
from typing import cast
import json


class Parser:
    def __init__(self, args: list[str]) -> None:
        self.__args_parser: ArgsParser = ArgsParser(args)
        self.__prompts: list[PromptModel]
        self.__function_defintions: list[FunctionDefinitionModel]

    def parse(self) -> None:
        self.__args_parser.parse()
        self.__parse_prompts()
        self.__parse_functions_definition()

    def __parse_functions_definition(self) -> None:
        functions_definition_file_content: str = Path(
            self.__args_parser.get_functions_definition_file
        ).read_text()
        function_definions_validator = FunctionsDefinitionRootModel.model_validate_json(
            functions_definition_file_content
        )
        self.__function_defintions = function_definions_validator.root

    def __parse_prompts(self) -> None:
        input_file_content: str = Path(
            self.__args_parser.get_input_file
        ).read_text()  # read the content
        prompts_validator = PromptsRootModel.model_validate(
            cast(str, json.loads(input_file_content))
        )  # validate the
        self.__prompts = prompts_validator.root

    @property
    def prompts(self) -> list[PromptModel]:
        return self.__prompts

    @property
    def functions_definition(self) -> list[FunctionDefinitionModel]:
        return self.__function_defintions

    def fns_def_names(self) -> set[str]:
        fns_def: set[str] = set()
        return fns_def

    @property
    def output_path(self) -> str:
        return self.__args_parser.get_output_file
