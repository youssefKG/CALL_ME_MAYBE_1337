import json
from pathlib import Path

from models.FunctionDefinitionJson import FunctionDefnitionModel

from .ArgParser import ArgsParser
from src.models.PromptJson import PromptJsonModel
from pydantic import TypeAdapter


class Parser:
    def __init__(self, args: list[str]) -> None:
        self.__args_parser: ArgsParser = ArgsParser(args)
        self.__prompts: set[str] = set()
        self.__function_defintions: list[str]

    def parse(self) -> None:
        self.__args_parser.parse()
        self.__parse_prompts()
        self.__parse_functions_definition()

    def __parse_functions_definition(self) -> None:
        functions_definition_file_content: str = Path(
            self.__args_parser.get_output_file
        ).read_text()
        function_defintion_model_adapter = TypeAdapter(list[FunctionDefnitionModel])
        function_definions: list[FunctionDefnitionModel] = (
            function_defintion_model_adapter.validate_json(
                self.__args_parser.get_functions_definition_file
            )
        )

    def __parse_prompts(self) -> None:
        input_file_content: str = Path(
            self.__args_parser.get_input_file
        ).read_text()  # read the content
        json_prompt_adapter = TypeAdapter(list[PromptJsonModel])
        prompts: list[PromptJsonModel] = json_prompt_adapter.validate_json(
            input_file_content
        )
        for prompt in prompts:
            self.__prompts.add(prompt.prompt)

    @property
    def get_prompts(self) -> set[str]:
        return self.__prompts
