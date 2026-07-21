from src.parser.parser import Parser
from src.LlmModel.model import Model
from src.generator.output_generator import OutputGenerator
from src.cache.cache import Cache
from src.prompts.prompt_generator import PromptGenerator

import sys


def main() -> None:
    model: Model = Model()
    parser: Parser = Parser(sys.argv)
    parser.parse()
    prompt_generator: PromptGenerator = (
        PromptGenerator.Builder()
        .set_function_definitions(parser.functions_definition)
        .set_function_name_static_prompt()
        .set_function_argument_static_prompt()
        .set_prompts(parser.prompts)
        .build()
    )
    _ = (  # singleton cache we init it
        Cache.Builder()
        .set_model(model)
        .set_function_name_static_prompt(prompt_generator.function_name_static_prompt)
        .set_tokens_ids()
        .set_function_argument_static_prompt(
            prompt_generator.function_argument_static_prompt
        )
        .build()
    )
    output_generator: OutputGenerator = OutputGenerator(
        parser.functions_definition,
        model,
        prompt_generator,
    )
    output_generator.generate()

    for function_call in output_generator.functions_calls:
        print("*" * 10)
        print(function_call.name)
        print(function_call.prompt)
        for argument in function_call.arguments.items():
            print(argument.name, " = ", argument.value)
        print("*" * 10)


if __name__ == "__main__":
    main()
