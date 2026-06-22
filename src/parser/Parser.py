from parser.ArgParser import ArgsParser


class Parser:
    def __init__(self, args: list[str]) -> None:
        self.args_parser: ArgsParser = ArgsParser(args)

    def parser(self) -> None:
        pass
