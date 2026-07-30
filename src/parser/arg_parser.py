from enum import Enum
from pathlib import Path
from typing import cast
from src.utils.file_checker import FileChecker


class ArgsError(Exception):
    pass


class DefaultFilePath(str, Enum):
    PROMPT_PATH = "data/input/function_calling_tests.json"
    FUNCTION_DEFINITION_PATH = "data/input/functions_definition.json"
    FUNCTION_CALL_PATH = "data/input/data/output/function_calls.json"


class ArgsParser:
    def __init__(self, args: list[str]) -> None:
        self.__args: list[str] = args[1:]
        self.__output_file: str | None = None
        self.__input_file_file: str | None = None
        self.__functions_definition_file: str | None = None
        self.__model_name: str = "Qwen/Qwen3-0.6B"

    def parse(self) -> None:
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
        if self.__functions_definition_file is not None:
            self.__raise_duplicated_option("--functions_definition")
        if file_path is None:
            self.__raise_missing_value_after_option("--input")
            return
        FileChecker.check_file_path_is_exist(file_path)
        FileChecker.check_file_is_readable(file_path)
        self.__functions_definition_file = file_path

    def __set_output_file(
        self, file_path: str | None = DefaultFilePath.FUNCTION_CALL_PATH.value
    ) -> None:
        if self.__output_file is None:
            self.__output_file = file_path
            output_file_path: Path = Path(cast(str, self.__output_file))
            output_file_path.touch(exist_ok=True)
        else:
            self.__raise_duplicated_option("output")

    def __set_input_file(
        self, file_path: str | None = DefaultFilePath.PROMPT_PATH.value
    ) -> None:
        if self.__input_file_file is not None:
            self.__raise_duplicated_option("--input")
        if file_path is None:
            return self.__raise_missing_value_after_option("--input")
        FileChecker.check_file_path_is_exist(file_path)
        FileChecker.check_file_is_readable(file_path)
        self.__input_file_file = file_path

    def __set_default_values(self) -> None:
        if self.__input_file_file is None:
            self.__set_input_file()
        if self.__output_file is None:
            self.__set_output_file()
        if self.__functions_definition_file is None:
            self.__raise_missing_functions_definition_file()

    def __set_model_name(self, model_name: str | None) -> None:
        if model_name:
            self.__model_name = model_name
        else:
            self.__raise_missing_value_after_option("--model_name")

    @property
    def get_output_file(self) -> str:
        return cast(str, self.__output_file)

    @property
    def get_input_file(self) -> str:
        return cast(str, self.__input_file_file)

    @property
    def get_functions_definition_file(self) -> str:
        return cast(str, self.__functions_definition_file)

    @property
    def model_name(self) -> str:
        return self.__model_name

    # ------------------------------ start Errors ---------------------------
    def __raise_unknown_option(self, option: str) -> None:
        raise ArgsError(
            f"Error: Unknown option '{option}'.\n"
            + " Allowed options are '-input' and"
            + " '--output' '--functions_definition.'"
        )

    def __raise_missing_value_after_option(self, option: str) -> None:
        raise ArgsError(
            f"Error: Missing value for option '{option}.'"
            + f" Expected a directory path after '{option}."
        )  # raise missing value after otpion

    def __raise_missing_functions_definition_file(self) -> None:
        raise ArgsError("Error: missing functions definition file from args")

    def __raise_duplicated_option(self, option: str) -> None:
        raise ArgsError(f"raise duplicated option {option}")


# ------------------------------ End Errors ---------------------------
