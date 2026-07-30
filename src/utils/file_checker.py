"""Helpers for validating that input and output files are usable."""

import os


class FileError(Exception):
    """Raised when a required file path is missing or inaccessible."""
    pass


class FileChecker:
    """Static helper methods for checking file readability and writability."""

    @staticmethod
    def check_file_is_readable(file_path: str) -> None:
        """Ensure that a file exists and can be read.

        Args:
            file_path: File path to validate.
        """
        is_readable: bool = os.access(file_path, os.R_OK)
        if not is_readable:
            raise FileError(
                f"FileError:\nUnable to open file '{file_path}.'"
                + "\nCheck that the file exists and that you"
                + "have sufficient permissions to read it."
            )

    @staticmethod
    def check_file_path_is_exist(file_path: str) -> None:
        """Ensure that a file path points to an existing file.

        Args:
            file_path: File path to validate.
        """
        is_exist: bool = os.access(file_path, os.F_OK)
        if not is_exist:
            raise FileError(
                f"FileError:\nOutput file '{file_path}' was not found.\nPlease"
                + "provide a valid path to an existing configuration file."
            )

    @staticmethod
    def check_file_is_writable(file_path: str) -> None:
        """Ensure that a file can be written to.

        Args:
            file_path: File path to validate.
        """
        is_writable: bool = os.access(file_path, os.W_OK)
        if not is_writable:
            raise FileError(
                f"Error: You do not have permission to write to {file_path}."
            )
