import pathlib

from .ArgParser import ArgsParser
from src.models.PromptJson import PromptJson



class Parser:
    def __init__(self, args: list[str]) -> None:
        self.__args_parser: ArgsParser = ArgsParser(args)

    def parse(self) -> None:
        self.__args_parser.parse()
        self.__validate_input_file()
        self.__validate_functions_definition_file()


    def __validate_functions_definition_file(self) -> None:
        pass

    def __validate_input_file(self) -> None:
        input_file_content: str = pathlib.Path(self.__args_parser.get_input_file).read_text()
        prompts: PromptJson = PromptJson.model_validate_json(input_file_content)
        print(prompts)
