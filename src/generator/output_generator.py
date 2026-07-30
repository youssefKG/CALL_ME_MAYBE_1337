"""Coordinate function-name and argument generation for a batch of prompts."""

from collections.abc import Generator

from src.models import (
    FunctionCallModel,
    PromptModel,
    FunctionCallRootModel,
    Argument,
    FunctionDefinitionModel,
)
from src.log import Log, LogRow
from src.predictors import FunctionParametersPredictor, FunctionNamePredictor
from src.llm.model import Model
from src.prompts.prompt_generator import PromptGenerator
from src.generator.function_name_generator import FunctionNameGenerator
from src.generator.function_parametre_generator import FunctionArgumentsGenerator
from src.cache import Cache


class OutputGenerator:
    """Generate function calls and persist them to disk as JSON."""

    def __init__(
        self,
        model: Model,
        /,
        *,
        log: Log,
        remaining_prompts: list[PromptModel],
        generated_functions_call: list[FunctionCallModel],
        functions_definitions: list[FunctionDefinitionModel],
        prompt_generator: PromptGenerator,
        output_path: str,
        cache: Cache,
    ) -> None:
        self.__functions_definitions: list[FunctionDefinitionModel] = (
            functions_definitions
        )
        self.__model: Model = model
        self.__prompt_generator: PromptGenerator = prompt_generator
        self.__remaining_prompts: list[PromptModel] = remaining_prompts
        self.__functions_calls: list[FunctionCallModel] = generated_functions_call
        self.__function_name_predictor: FunctionNamePredictor
        self.__function_parameters_predictor: FunctionParametersPredictor = (
            FunctionParametersPredictor(cache=cache)
        )
        self.__output_path: str = output_path
        self.__log: Log = log
        self.__cache: Cache = cache
        self.__init_functions_name_predictor()

    def generate(self) -> None:
        """Generate outputs for all remaining prompts.

        Returns:
            None
        """
        for prompt in self.__iter_prompts():
            self.__log.add_row(
                LogRow(prompt.id, prompt.prompt, "Generating..."),
                status=f"{prompt.id}-Generating function definition",
            )
            function_definition: FunctionDefinitionModel | None = (
                self.__function_definition(prompt.prompt)
            )
            if function_definition:
                function_call: FunctionCallModel = FunctionCallModel(
                    name=function_definition.name,
                    prompt=prompt.prompt,
                    parameters=self.__function_arguments(function_definition, prompt),
                )
                self.__functions_calls.append(function_call)
                self.__log.add_row(
                    LogRow(
                        prompt.id,
                        prompt.prompt,
                        function_definition.model_dump_json(indent=4),
                        function_call.model_dump_json(indent=4),
                    )
                )
            self.__generate_output_file()

    def __function_definition(self, prompt: str) -> FunctionDefinitionModel | None:
        """Infer the best matching function definition for a prompt.

        Args:
            prompt: User prompt to resolve.

        Returns:
            FunctionDefinitionModel | None: Matching function schema if one is found.
        """

        def __get_function_definition(
            function_name: str,
        ) -> FunctionDefinitionModel | None:
            for function_def in self.__functions_definitions:
                if function_def.name == function_name:
                    return function_def
            return None

        function_name_generator: FunctionNameGenerator = FunctionNameGenerator(
            self.__model,
            cache=self.__cache,
            function_name_predictor=self.__function_name_predictor,
            prompt_generator=self.__prompt_generator,
            prompt=prompt,
        )
        function_name_generator.generate()
        return __get_function_definition(function_name_generator.fn_name)

    def __function_arguments(
        self, function_definition: FunctionDefinitionModel, prompt: PromptModel
    ) -> Argument:
        function_argument_generator = FunctionArgumentsGenerator(
            self.__model,
            cache=self.__cache,
            prompt_generator=self.__prompt_generator,
            user_prompt=prompt,
            function_definition=function_definition,
            function_parameters_predictor=self.__function_parameters_predictor,
            log=self.__log,
        )
        function_argument_generator.generate()
        return function_argument_generator.function_arguments

    def __init_functions_name_predictor(self) -> None:
        """Initialize the trie used to constrain function-name generation."""
        self.__function_name_predictor = FunctionNamePredictor()
        fns_def_names_ids: list[list[int]] = list()
        for fn_def in self.__functions_definitions:
            fns_def_names_ids.append(self.__model.encode_text(fn_def.name))
        self.__function_name_predictor.set_fns_names_ids_trie(fns_def_names_ids)

    @property
    def functions_calls(self) -> list[FunctionCallModel]:
        """Get the generated function-call objects.

        Returns:
            list[FunctionCallModel]: Generated function calls.
        """
        return self.__functions_calls

    def __generate_output_file(self) -> None:
        """Write the current function-call batch to the configured output file."""
        try:
            with open(self.__output_path, "w") as output_file:
                functions_calls_json: str = FunctionCallRootModel(
                    self.__functions_calls
                ).model_dump_json(indent=4)
                output_file.write(functions_calls_json)
        except Exception:
            pass

    def __iter_prompts(self) -> Generator[PromptModel]:
        """Yield remaining prompts to process.

        Yields:
            PromptModel: The next prompt in the queue.
        """
        for prompt in self.__remaining_prompts:
            yield prompt
