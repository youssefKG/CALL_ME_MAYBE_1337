from src.Parser.Parser import Parser
from src.prompts.prompt_generator import PromptGenerator
from src.generator.generator import Generator, OutputGenerator
from collections.abc import Generator

import sys


def main() -> None:
    parser: Parser = Parser(sys.argv)
    parser.parse()
    output_generator: OutputGenerator = OutputGenerator(parser)
    fn_name_generator: Generator[str | None] = output_generator.generate()
    fn_name = next(fn_name_generator)
    while fn_name:
        print(fn_name)
        fn_name = next(fn_name_generator)


if __name__ == "__main__":
    main()
