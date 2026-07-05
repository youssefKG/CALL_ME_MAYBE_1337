from src.Parser.Parser import Parser
from src.prompts.prompt_generator import PromptGenerator
from src.generator.generator import Generator

import sys


def main() -> None:
    parser: Parser = Parser(sys.argv)
    parser.parse()
    generator: Generator = Generator(parser)
    prompt: str = generator.next_prompt
    text_ids_generator: callable = generator.generate_prompt_ids(prompt)
    text_ids = text_ids_generator()
    for _ in range(10):
        token, token_id = generator.get_next_token(text_ids)
        text_ids = text_ids_generator(token_id)
        print(token, end="")


if __name__ == "__main__":
    main()
