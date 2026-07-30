"""Utilities for displaying generation progress in the console."""

from rich.console import Console
from rich.table import Table
from src.models.prompt_model import PromptModel

import sys
import os


class LogRow:
    """Represents one row of progress information in the live log.

    Attributes:
        id: Unique identifier for this log entry.
        prompt: The user's input prompt text.
        function_defintion: The selected function definition.
        function_call: The generated function call.
    """
    def __init__(
        self,
        id: str,
        prompt: str,
        function_defintion: str = "",
        function_call: str = "",
    ) -> None:
        """Initialize a log row with prompt and generation results.

        Args:
            id: Unique identifier for this row.
            prompt: User's input prompt text.
            function_defintion: Selected function definition (default "").
            function_call: Generated function call (default "").
        """
        self.prompt: str = prompt
        self.function_defintion: str = function_defintion
        self.function_call: str = function_call
        self.id: str = id


class Log:
    """Render a live table of prompt progress and generated function calls.

    Maintains a table showing the status of each prompt as it moves through
    the generation pipeline. Updates the console display in real-time.
    """
    def __init__(self) -> None:
        """Initialize the log with empty state.

        Attributes:
            __console: Rich console for formatted output.
            __rows: Mapping of prompt IDs to their log rows.
        """
        self.__console: Console = Console()
        self.__rows: dict[str, LogRow] = dict()

    def __update(self) -> None:
        """Refresh the console table with the latest rows.

        Clears the console and redisplays the table with the current state
        of all rows using rich formatting.
        """
        os.system("cls" if os.name == "nt" else "clear")
        table: Table = Table(title="CALL_ME_BABY", show_lines=True)
        table.add_column("Id", no_wrap=False, width=30)
        table.add_column("Prompt", no_wrap=False, width=40)
        table.add_column("Function Definition", no_wrap=False, width=80)
        table.add_column("Funtion Call", no_wrap=False, width=80)
        for id, row in self.__rows.items():
            table.add_row(
                f"{id}",
                f"[green]{row.prompt}",
                f"[magenta]{row.function_defintion}",
                f"{row.function_call}",
            )
        self.__console.print(table)
        sys.stdout.flush()

    def add_row(self, row: LogRow, status: str = "") -> None:
        """Add or update a log row and print the latest state.

        Args:
            row: Row data to store.
            status: Optional status message to print below the table.
        """
        self.__rows[row.id] = row
        self.__update()
        self.__console.print(status)

    def add_rows(self, rows: list[LogRow]) -> None:
        """Add several rows to the log in one pass.

        Args:
            rows: Rows to initialize in the log.
        """
        for row in rows:
            self.__rows[row.id] = row
        self.__update()

    def init_prompts(self, prompts: list[PromptModel]) -> None:
        """Seed the log with one row per prompt before generation starts.

        Args:
            prompts: Prompt objects to initialize.
        """
        for prompt in prompts:
            self.__rows[prompt.id] = LogRow(prompt.id, prompt.prompt)
