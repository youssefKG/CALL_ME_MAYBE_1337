"""Parse and validate command-line arguments for the generation pipeline."""

from enum import Enum
from pathlib import Path
from typing import cast
from src.utils.file_checker import FileChecker
import os


class ArgsError(Exception):
    """Raised when the command-line arguments are invalid or incomplete."""
    pass


class DefaultFilePath(str, Enum):
    """Default input and output file paths used when the user omits CLI arguments."""
    PROMPT_PATH = "data/input/function_calling_tests.json"
    FUNCTION_DEFINITION_PATH = "data/input/functions_definition.json"
    FUNCTION_CALL_PATH = "data/input/output/function_calls.json"


class ArgsParser:
    """Parse CLI options for input, output, function definitions, and model selection."""
    def __init__(self, args: list[str]) -> None:
        """Initialize the parser with the raw CLI argument list.

        Args:
            args: List of CLI arguments including the program name.
        """
        self.__args: list[str] = args[1:]
        self.__output_file: str | None = None
        self.__input_file_file: str | None = None
        self.__functions_definition_file: str | None = None
        self.__model_name: str = "Qwen/Qwen3-0.6B"

    def parse(self) -> None:
        """Parse and validate the CLI arguments.

        Returns:
            None
        """
        idx: int = 0
        while idx < len(self.__args):
            option: str = self.__args[idx]
            arg_value: str | None = (
                self.__args[idx + 1] if idx + 1 < len(self.__args) else None
            )
            self.__set_arg_value(option, arg_value)
            idx += 2
        self.__set_default_values()

    def __set_arg_value(self, option: str, arg_value: str | None = None) -> None:
        """Route a parsed option to its corresponding setter.

        Args:
            option: CLI option name.
            arg_value: Optional value provided after the option.
        """
        match option:
            case "--input":
                self.__set_input_file(arg_value)
            case "--output":
                self.__set_output_file(arg_value)
            case "--functions_definition":
                self.__set_functions_definition_file(arg_value)
            case "--model_name":
                self.__set_model_name(arg_value)
            case _:
                self.__raise_unknown_option(option)

    def __set_functions_definition_file(
        self, file_path: str | None = DefaultFilePath.FUNCTION_DEFINITION_PATH.value
    ) -> None:
        """Store and validate the path to the function-definition JSON file.

        Args:
            file_path: Path to the function-definition file.
        """
        if self.__functions_definition_file is not None:
            self.__raise_duplicated_option("--functions_definition")
        self.__functions_definition_file = file_path
        FileChecker.check_file_path_is_exist(
            cast(str, self.__functions_definition_file)
        )
        FileChecker.check_file_is_readable(cast(str, self.__functions_definition_file))
        self.__functions_definition_file = file_path

    def __set_output_file(
        self, file_path: str | None = DefaultFilePath.FUNCTION_CALL_PATH.value
    ) -> None:
        """Store and prepare the output file path for generated function calls.

        Args:
            file_path: Output JSON file path.
        """
        if self.__output_file is None:
            self.__output_file = file_path
            is_exist: bool = os.access(cast(str, self.__output_file), os.F_OK)
            if is_exist and self.__output_file is not None:
                FileChecker.check_file_is_readable(self.__output_file)
                FileChecker.check_file_is_writable(self.__output_file)
            output_file_path: Path = Path(cast(str, self.__output_file))
            output_file_path.parent.mkdir(exist_ok=True, parents=True)
            output_file_path.touch(exist_ok=True)
        else:
            self.__raise_duplicated_option("output")

    def __set_input_file(
        self, file_path: str | None = DefaultFilePath.PROMPT_PATH.value
    ) -> None:
        """Store and validate the path to the input prompt JSON file.

        Args:
            file_path: Path to the input prompt file.
        """
        if self.__input_file_file is not None:
            self.__raise_duplicated_option("--input")
        if file_path is None:
            return self.__raise_missing_value_after_option("--input")
        FileChecker.check_file_path_is_exist(file_path)
        FileChecker.check_file_is_readable(file_path)
        self.__input_file_file = file_path

    def __set_default_values(self) -> None:
        """Populate missing CLI values with the built-in defaults."""
        if self.__input_file_file is None:
            self.__set_input_file()
        if self.__output_file is None:
            self.__set_output_file()
        if self.__functions_definition_file is None:
            self.__set_functions_definition_file()

    def __set_model_name(self, model_name: str | None) -> None:
        """Store the selected model name, if one was provided.

        Args:
            model_name: Model identifier supplied by the user.
        """
        if model_name:
            self.__model_name = model_name
        else:
            self.__raise_missing_value_after_option("--model_name")

    @property
    def get_output_file(self) -> str:
        """Get the resolved output file path.

        Returns:
            str: Output JSON path.
        """
        return cast(str, self.__output_file)

    @property
    def get_input_file(self) -> str:
        """Get the resolved input prompt file path.

        Returns:
            str: Input JSON path.
        """
        return cast(str, self.__input_file_file)

    @property
    def get_functions_definition_file(self) -> str:
        """Get the resolved function-definition file path.

        Returns:
            str: Functions-definition JSON path.
        """
        return cast(str, self.__functions_definition_file)

    @property
    def model_name(self) -> str:
        """Get the configured model identifier.

        Returns:
            str: Model name.
        """
        return self.__model_name

    # ------------------------------ start Errors ---------------------------
    def __raise_unknown_option(self, option: str) -> None:
        """Raise an error for an unsupported CLI option.

        Args:
            option: Unknown option name.
        """
        raise ArgsError(
            f"Error: Unknown option '{option}'.\n"
            + " Allowed options are '-input' and"
            + " '--output' '--functions_definition.'"
        )

    def __raise_missing_value_after_option(self, option: str) -> None:
        """Raise an error when an option is missing its required value.

        Args:
            option: Option that is missing a value.
        """
        raise ArgsError(
            f"Error: Missing value for option '{option}.'"
            + f" Expected a directory path after '{option}."
        )  # raise missing value after otpion

    def __raise_missing_functions_definition_file(self) -> None:
        """Raise an error when the function-definition file is missing."""
        raise ArgsError("Error: missing functions definition file from args")

    def __raise_duplicated_option(self, option: str) -> None:
        """Raise an error when a CLI option is supplied more than once.

        Args:
            option: Repeated option name.
        """
        raise ArgsError(f"raise duplicated option {option}")


# ------------------------------ End Errors ---------------------------
