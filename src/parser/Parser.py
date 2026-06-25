from pathlib import Path

from src.models.FunctionDefinitionJson import FunctionDefinitionModel

from .ArgParser import ArgsParser
from src.models.PromptJson import PromptsRootModel


class Parser:
    def __init__(self, args: list[str]) -> None:
        self.__args_parser: ArgsParser = ArgsParser(args)
        self.__prompts: PromptsRootModel
        self.__function_defintions: FunctionDefinitionModel

    def parse(self) -> None:
        self.__args_parser.parse()
        self.__parse_prompts()
        self.__parse_functions_definition()

    def __parse_functions_definition(self) -> None:
        functions_definition_file_content: str = Path(
            self.__args_parser.get_functions_definition_file
        ).read_text()
        function_definions_validator = FunctionDefinitionModel.model_validate_json(
            functions_definition_file_content
        )
        self.__function_defintions = function_definions_validator.model_dump()

    def __parse_prompts(self) -> None:
        print(self.__args_parser.get_input_file)
        input_file_content: str = Path(
            self.__args_parser.get_input_file
        ).read_text()  # read the content
        prompts_validator = PromptsRootModel.model_validate_json(input_file_content)
        self.__prompts = prompts_validator.model_dump()

    @property
    def get_prompts(self) -> PromptsRootModel:
        return self.__prompts

    @property
    def get_functions_defintions(self) -> FunctionDefinitionModel:
        return self.__function_defintions
