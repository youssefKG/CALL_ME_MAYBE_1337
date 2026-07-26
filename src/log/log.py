from rich.console import Console
from rich.table import Table
from typing_extensions import Self

import sys
import os

"""

TABLE_DATA = [
    [
        "[b white]DSA Course[/]: [i]Beginner[/]",
        "[magenta]$[/]10",
        "[green]Geeks for Geeks[/]",
        "15 hours",
    ],
    [
        "[b white]DSA Course[/]: [i]Intermediate[/]",
        "[magenta]$[/]20",
        "[green]Geeks for Geeks[/]",
        "25 hours",
    ],
    [
        "[b white]DSA Course[/]: [i]Advanced[/]",
        "[magenta]$[/]30",
        "[green]Geeks for Geeks[/]",
        "30 hours",
    ],
    [
        "[b white]Operating System Fundamentals[/]",
        "[magenta]$[/]25",
        "[green]Geeks for Geeks[/]",
        "35 hours",
    ],
]

console = Console()


table = Table(show_footer=False)
table_centered = Align.center(table)

console.clear()

with Live(table_centered, console=console, screen=False):
    table.add_column("Course Name", no_wrap=True)
    table.add_column("Price", no_wrap=True)
    table.add_column("Organization", no_wrap=True)
    table.add_column("Duration", no_wrap=True)
    for row in TABLE_DATA:
        table.add_row(*row)

    table_width = console.measure(table).maximum

    table.width = None

table = Table(title="Star Wars Movies")

table.add_column("Released", justify="right", style="cyan", no_wrap=True)
table.add_column("Title", style="magenta")
table.add_column("Box Office", justify="right", style="green")

table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

console = Console()
console.print(table)

"""


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
