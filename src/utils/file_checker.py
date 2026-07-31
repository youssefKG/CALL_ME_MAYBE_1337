"""Helpers for validating that input and output files are usable."""

import os


class FileError(Exception):
    """Raised when a required file path is missing or inaccessible.

    This exception is raised when file validation checks fail, indicating
    that a file cannot be accessed for reading, writing, or verification.
    """

    pass


class FileChecker:
    """Static helper methods for checking file readability and writability.

    Provides utilities to validate file accessibility before use in the
    pipeline, ensuring robust error handling for file I/O operations.
    """

    @staticmethod
    def check_file_is_readable(file_path: str) -> None:
        """Ensure that a file exists and can be read.

        Verifies that the specified file exists and has read permissions
        for the current process. Raises FileError if these conditions
        are not met.

        Args:
            file_path: File path to validate.

        Raises:
            FileError: If file is missing or not readable.
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

        Checks whether a file exists at the given path. Raises FileError
        if the path does not point to an existing file.

        Args:
            file_path: File path to validate.

        Raises:
            FileError: If file does not exist.
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

        Verifies that the specified file has write permissions for the
        current process. Raises FileError if write access is denied.

        Args:
            file_path: File path to validate.

        Raises:
            FileError: If file is not writable.
        """
        is_writable: bool = os.access(file_path, os.W_OK)
        if not is_writable:
            raise FileError(
                f"Error: You do not have permission to write to {file_path}."
            )
