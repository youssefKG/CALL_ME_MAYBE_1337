from src.error_recovery.error_recovery import ErrorRecovery
from src.parser import Parser
from src.llm.model import Model
from src.generator import OutputGenerator
from src.cache import Cache
from src.prompts import PromptGenerator
from src.log import Log

import sys


def main() -> None:
    parser: Parser = Parser(sys.argv)
    parser.parse()
    model: Model = Model(parser.model_name)
    log: Log = Log()
    log.init_prompts(parser.prompts)
    prompt_generator: PromptGenerator = (
        PromptGenerator.Builder()
        .set_function_definitions(parser.functions_definition)
        .set_function_name_static_prompt()
        .set_function_argument_static_prompt()
        .set_prompts(parser.prompts)
        .build()
    )
    (
        Cache.Builder()
        .set_model(model)
        .set_function_name_static_prompt(prompt_generator.function_name_static_prompt)
        .set_tokens_ids()
        .set_function_argument_static_prompt(
            prompt_generator.function_argument_static_prompt
        )
        .build()
    )
    error_recovery: ErrorRecovery = ErrorRecovery(
        log=log,
        output_path=parser.output_path,
        function_definitions=parser.functions_definition,
        prompts=parser.prompts,
    )
    error_recovery.recover()
    output_generator: OutputGenerator = OutputGenerator(
        model,
        log=log,
        remaining_prompts=error_recovery.remaining_prompts,
        generated_functions_call=error_recovery.generated_functions_calls,
        functions_definitions=parser.functions_definition,
        prompt_generator=prompt_generator,
        output_path=parser.output_path,
    )
    output_generator.generate()


if __name__ == "__main__":
    main()
