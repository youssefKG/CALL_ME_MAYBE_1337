"""Parse CLI arguments, prompts, and function definitions for the generation pipeline."""

from pathlib import Path

from pydantic import ValidationError
from src.models.function_definition_model import (
    FunctionsDefinitionRootModel,
    FunctionDefinitionModel,
)
from .arg_parser import ArgsParser
from src.models.prompt_model import PromptModel, PromptsRootModel
import sys


class Parser:
    """Validate and expose configuration parsed from the CLI and input files.

    Orchestrates parsing of command-line arguments, input prompts, and
    function definitions. Validates JSON inputs and makes parsed data
    available via properties.

    Attributes:
        __args_parser: CLI argument parser.
        __prompts: Loaded prompt objects.
        __function_defintions: Loaded function definitions.
        __model_name: Selected model identifier.
    """

    def __init__(self, args: list[str]) -> None:
        """Initialize parser with CLI arguments.

        Args:
            args: Command-line arguments including program name.
        """
        self.__args_parser: ArgsParser = ArgsParser(args)
        self.__prompts: list[PromptModel]
        self.__function_defintions: list[FunctionDefinitionModel]
        self.__model_name: str

    def parse(self) -> None:
        """Parse arguments, prompts, and function definitions.

        Orchestrates the complete parsing pipeline: processes CLI args,
        loads and validates prompt and function-definition JSON files,
        and extracts the model name.

        Returns:
            None
        """
        self.__args_parser.parse()
        self.__parse_prompts()
        self.__parse_functions_definition()
        self.__parse_model_name()

    def __parse_functions_definition(self) -> None:
        """Load and validate the JSON file that defines available functions.

        Reads the function-definition JSON file, parses it using Pydantic,
        and stores the resulting function definitions. Exits on validation
        error.

        Returns:
            None
        """
        functions_definition_file_content: str = Path(
            self.__args_parser.get_functions_definition_file
        ).read_text()
        try:
            function_definions_validator = (
                FunctionsDefinitionRootModel.model_validate_json(
                    functions_definition_file_content
                )
            )
            self.__function_defintions = function_definions_validator.root
        except ValidationError as error:
            print(
                f"Validation Error({self.__args_parser.get_functions_definition_file}):\n",
                f"{error.errors()[0]['msg']}",
            )
            sys.exit(1)

    def __parse_model_name(self) -> None:
        """Store the model name selected from the CLI arguments.

        Extracts the model name from the parsed CLI arguments and stores
        it for later access.

        Returns:
            None
        """
        self.__model_name = self.__args_parser.model_name

    def __parse_prompts(self) -> None:
        """Load and validate the prompt dataset from the input JSON file.

        Reads the prompt JSON file, parses it using Pydantic, and stores
        the resulting prompt objects. Exits on validation error.

        Returns:
            None
        """
        input_file_content: str = Path(
            self.__args_parser.get_input_file
        ).read_text()  # read the content
        try:
            prompts_validator = PromptsRootModel.model_validate_json(
                input_file_content
            )
            self.__prompts = prompts_validator.root
        except ValidationError as error:
            print(
                f"Validation Error({self.__args_parser.get_input_file}):\n",
                f"{error.errors()[0]['msg']}",
            )
            sys.exit(1)

    @property
    def prompts(self) -> list[PromptModel]:
        """Get the validated prompt objects.

        Returns:
            list[PromptModel]: Parsed prompts for generation.
        """
        return self.__prompts

    @property
    def functions_definition(self) -> list[FunctionDefinitionModel]:
        """Get the validated function definitions.

        Returns:
            list[FunctionDefinitionModel]: Available functions for the run.
        """
        return self.__function_defintions

    def fns_def_names(self) -> set[str]:
        fns_def: set[str] = set()
        return fns_def

    @property
    def output_path(self) -> str:
        """Get the output path for the generated function-call JSON.

        Returns:
            str: Path to the output file.
        """
        return self.__args_parser.get_output_file

    @property
    def model_name(self) -> str:
        """Get the configured model name.

        Returns:
            str: Name of the language model to use.
        """
        return self.__model_name
