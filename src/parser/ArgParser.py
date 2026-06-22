from enum import Enum
from typing import cast
import os


class ArgsError(Exception):
    pass


class DefaultFilePath(str, Enum):
    INPUT_FILE = "data/input/functions_definition.json"
    OUTPUT_FILE = "data/output/function_calls.json"


class ArgsParser:
    def __init__(self, args: list[str]) -> None:
        self.args: list[str] = args[2:]
        self.output_file: str | None = None
        self.input_file: str | None = None
        self.functions_definition_file: str | None = None

    def parse(self) -> None:
        idx: int = 0
        while idx < len(self.args):
            option: str = self.args[idx]
            file_path: str | None = (
                self.args[idx + 1] if idx + 1 < len(self.args) else None
            )
            self.__set_file(option, file_path)
            idx += 2
        self.__set_default_values()

    def __set_file(self, option: str, file_path: str | None) -> None:
        match option:
            case "--input":
                self.__set_function_definitions_file(file_path)
            case "--output":
                self.__set_input_file(file_path)
            case "--functions_definition":
                self.__set_output_file(file_path)
            case _:
                self.__raise_unknown_option(option)

    def __set_function_definitions_file(self, file_path: str | None) -> None:
        if self.functions_definition_file is not None:
            self.__raise_duplicated_option("output")
        if file_path is None:
            self.__raise_missing_value_after_option("--functions-definition")
        self.functions_definition_file = file_path

    def __set_output_file(
        self, file_path: str | None = DefaultFilePath.OUTPUT_FILE.value
    ) -> None:
        if self.output_file is not None:
            self.__raise_duplicated_option("output")
        if file_path is None:
            self.__raise_missing_value_after_option("--output")
            return
        self.output_file = file_path

    def __set_input_file(
        self, file_path: str | None = DefaultFilePath.INPUT_FILE.value
    ) -> None:
        if self.input_file is not None:
            self.__raise_duplicated_option("--input")
        if file_path is None:
            self.__raise_missing_value_after_option("--input")
            return
        self.__check_file_path_is_exist(file_path)
        self.__check_file_is_readable(file_path)
        self.input_file = file_path

    def __set_default_values(self) -> None:
        if self.input_file is None:
            self.__set_input_file()
        if self.output_file is None:
            self.__set_output_file()
        if self.functions_definition_file is None:
            self.__raise_missing_functions_definition_file()

    @property
    def get_output_file(self) -> str:
        return cast(str, self.output_file)

    @property
    def get_input_file(self) -> str:
        return cast(str, self.input_file)

    @property
    def get_functions_definition_file(self) -> str:
        return cast(str, self.functions_definition_file)

    def __check_file_is_readable(self, file_path: str) -> None:
        is_readable: bool = os.access(file_path, os.R_OK)
        if not is_readable:
            self.__raise_connot_open_file(file_path)

    def __check_file_path_is_exist(self, file_path: str) -> None:
        is_exist: bool = os.access(file_path, os.F_OK)
        if not is_exist:
            self.__raise_invalid_file_path(file_path)

    # ---------------------------- Errors -------------------------
    def __raise_invalid_file_path(self, file_path: str) -> None:
        raise ArgsError(
            f"FileError:\nMap file '{file_path}' was not found.\nPlease"
            + "provide a valid path to an existing configuration file."
        )

    def __raise_connot_open_file(self, file_path: str) -> None:
        raise ArgsError(
            f"FileError:\nUnable to open file '{file_path}.'"
            + "\nCheck that the file exists and that you"
            + "have sufficient permissions to read it."
        )

    def __raise_unknown_option(self, option: str) -> None:
        raise ArgsError(
            f"Error: Unknown option '{option}'.\n"
            + " Allowed options are '--input' and"
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
