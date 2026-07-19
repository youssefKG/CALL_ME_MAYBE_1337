from src.parser.parser import Parser
from src.LlmModel.model import Model
from src.generator.output_generator import OutputGenerator
from src.cache.cache import Cache
from src.prompts.prompt_generator import PromptGenerator

import sys

from src.utils.function import FunctionCall


def main() -> None:
    parser: Parser = Parser(sys.argv)
    parser.parse()
    model: Model = Model()
    prompt_generator: PromptGenerator = PromptGenerator.Builder()
    cache: Cache = Cache.Builder(model).set_function_argument_static_prompt


if __name__ == "__main__":
    main()
