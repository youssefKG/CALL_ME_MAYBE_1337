from src.parser.parser import Parser
from src.generator.output_generator import OutputGenerator
from collections.abc import Generator

import sys

from src.utils.function import FunctionCall


def main() -> None:
    parser: Parser = Parser(sys.argv)
    parser.parse()
    output_generator: OutputGenerator = OutputGenerator(parser)
    fn_name_generator: Generator[FunctionCall | None] = output_generator.generate()
    function_call: FunctionCall | None = next(fn_name_generator)
    while function_call:
        function_call = next(fn_name_generator)


if __name__ == "__main__":
    main()
