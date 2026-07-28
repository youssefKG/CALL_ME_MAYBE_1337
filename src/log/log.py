from rich.console import Console
from rich.table import Table
from typing_extensions import Self

import sys
import os


class LogRow:
    def __init__(
        self,
        id: int,
        prompt: str,
        function_defintion: str = "",
        function_call: str = "",
    ) -> None:
        self.prompt: str = prompt
        self.function_defintion: str = function_defintion
        self.function_call: str = function_call
        self.id: int = id


class Log:
    __instance: Self | None = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self) -> None:
        self.__console: Console = Console()
        self.__rows: dict[int, LogRow] = dict()

    def __update(self) -> None:
        os.system("cls" if os.name == "nt" else "clear")
        table: Table = Table(title="CALL_ME_BABY", show_lines=True)
        table.add_column("Prompt", no_wrap=False, width=40)
        table.add_column("Function Definition", no_wrap=False, width=80)
        table.add_column("Funtion Call", no_wrap=False, width=80)
        for id, row in self.__rows.items():
            table.add_row(
                f"{id}-[green]{row.prompt}",
                f"[magenta]{row.function_defintion}",
                f"{row.function_call}",
            )
        self.__console.print(table)
        sys.stdout.flush()

    def add_row(self, row: LogRow, status: str = "") -> None:
        self.__rows[row.id] = row
        self.__update()
        self.__console.print(status)

    def add_rows(self, rows: list[LogRow]) -> None:
        for row in rows:
            self.__rows[row.id] = row
        self.__update()
