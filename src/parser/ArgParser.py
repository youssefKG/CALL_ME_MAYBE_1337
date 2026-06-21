from enum import Enum, auto
import os


class ArgsError(Exception):
    pass


class ArgOption(Enum):
    FUNCTION_DEFINITION = auto()
    OUTPUT_FILE = auto()
    INPUT_FILE = auto()
    UNKNOWN = auto()


class DefaulFilePaths(Enum, str):
    INPUT_FILE = ""


class ArgsParser:
    def __init__(self, args: list[str]) -> None:
        self.args: list[str] = args[2:]
        self.output_file: str = "data/output/function_calls.json"
        self.input_file: str = "data/input/functions_definition.json"
        self.functions_definition_file: str | None = None

    def parse(self) -> None:
        pass

    def __set_function_definitions_file(self, file_path: str) -> None:
        self.functions_definition_file = file_path

    def __set_output_file(self, file_path: str) -> None:
        self.__check_file_permision_existance(file_path)
        self.output_file = file_path

    def __set_input_file(self, file_path: str) -> None:
        self.__check_file_permision_existance(file_path)
        self.input_file = file_path

    def __set_file(self, option: str, file_path: str) -> None:
        match option:
            case "--input":
                self.__set_function_definitions_file(file_path)
            case "--output":
                self.__set_input_file(file_path)
            case "--functions_definition":
                self.__set_output_file(file_path)
            case _:
                self.__raise_unknown_option(option)

    def __check_file_permision_existance(self, file_path: str) -> None:
        is_exist: bool = os.access(file_path, os.F_OK)
        if not is_exist:
            self.__raise_invalid_file_path(file_path)
        is_readable: bool = os.access(file_path, os.R_OK)
        if not is_readable:
            self.__raise_connot_open_file(file_path)

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
