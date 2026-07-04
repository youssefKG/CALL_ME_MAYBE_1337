from src.Parser.Parser import Parser
from src.prompts.prompt_generator import PromptGenerator
from src.generator.generator import Generator

import sys


def main() -> None:
    parser: Parser = Parser(sys.argv)
    parser.parse()
    generator: Generator = Generator(parser)
    generator.init_cache()
    text_ids: list[int] = generator.generate_prompt_ids()
    next_token = generator.get_next_token(text_ids)
    print(next_token)

if __name__ == "__main__":
    main()
