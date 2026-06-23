from enum import Enum
from typing import cast
from src.utils.FileChecker import FileChecker

class ArgsError(Exception):
    pass


class DefaultFilePath(str, Enum):
    INPUT_FILE = "data/input/functions_definition.json"
    OUTPUT_FILE = "data/output/function_calls.json"


class ArgsParser:
    def __init__(self, args: list[str]) -> None:
        self.__args: list[str] = args[1:]
        self.__output_file: str | None = None
        self.__input_file_file: str | None = None
        self.__functions_definition_file: str | None = None

    def parse(self) -> None:
        idx: int = 0
        while idx < len(self.__args):
            option: str = self.__args[idx]
            file_path: str | None = (
                self.__args[idx + 1] if idx + 1 < len(self.__args) else None
            )
            self.__set_file(option, file_path)
            idx += 2
        self.__set_default_values()

    def __set_file(self, option: str, file_path: str | None) -> None:
        match option:
            case "--input":
                self.__set_input_file(file_path)
            case "--output":
                self.__set_output_file(file_path)
            case "--functions_definition":
                self.__set_functions_definition_file(file_path)
            case _:
                self.__raise_unknown_option(option)

    def __set_functions_definition_file(self, file_path: str | None) -> None:
        if self.__functions_definition_file is not None:
            self.__raise_duplicated_option("--functions_definition")
        if file_path is None:
            self.__raise_missing_value_after_option("--functions-definition")
        self.__functions_definition_file = file_path

    def __set_output_file(
        self, file_path: str | None = DefaultFilePath.OUTPUT_FILE.value
    ) -> None:
        if self.__output_file is not None:
            self.__raise_duplicated_option("output")
        if file_path is None:
            self.__raise_missing_value_after_option("--output")
            return
        self.__output_file = file_path

    def __set_input_file(
        self, file_path: str | None = DefaultFilePath.INPUT_FILE.value
    ) -> None:
        if self.__input_file_file is not None:
            self.__raise_duplicated_option("--input")
        if file_path is None:
            self.__raise_missing_value_after_option("--input")
            return
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

    @property
    def get_output_file(self) -> str:
        return cast(str, self.__output_file)

    @property
    def get_input_file(self) -> str:
        return cast(str, self.__input_file_file)

    @property
    def get_functions_definition_file(self) -> str:
        return cast(str, self.__functions_definition_file)

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
