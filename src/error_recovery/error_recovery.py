"""Recover from invalid or incomplete generated outputs during a run."""

from pydantic import ValidationError

from src.log.log import Log, LogRow
from src.models.function_definition_model import (
    FunctionDefinitionModel,
)
from src.models.prompt_model import PromptModel
from src.models import FunctionCallModel, FunctionCallRootModel
from pathlib import Path


class ErrorRecovery:
    """Validate previous outputs and continue for unfinished prompts.

    Manages recovery from interrupted generation runs by validating
    previously saved output and determining which prompts still need
    processing. Implements checkpoint-and-resume functionality.

    Attributes:
        __output_path: Path to the output JSON file.
        __functions_definitions: List of available function definitions.
        __prompts: All input prompts for this batch.
        __generated_functions_call: Recovered valid function calls.
        __generated_prompts: Prompts that have been fully processed.
        __remaining_prompts: Prompts still needing generation.
        __log: Logger for displaying progress.
    """

    def __init__(
        self,
        *,
        log: Log,
        output_path: str,
        function_definitions: list[FunctionDefinitionModel],
        prompts: list[PromptModel],
    ) -> None:
        """Initialize error recovery with configuration.

        Args:
            log: Logger instance for displaying recovery progress.
            output_path: Path to the persisted output JSON file.
            function_definitions: Available function definitions.
            prompts: All prompts for this generation batch.
        """
        self.__output_path: str = output_path
        self.__functions_definitions: list[FunctionDefinitionModel] = (
            function_definitions
        )
        self.__prompts: list[PromptModel] = prompts
        self.__generated_functions_call: list[FunctionCallModel] = list()
        self.__generated_prompts: list[str] = list()
        self.__remaining_prompts: list[PromptModel] = list()
        self.__log: Log = log
        self.__init_log()

    def recover(self) -> None:
        """Restore valid prior output or reset for invalid persisted state.

        Attempts to load the previous output file and validate all saved
        function calls. If any are invalid, resets to start from scratch.
        Updates remaining_prompts to only include unfinished items.

        Returns:
            None
        """
        function_defintion: FunctionDefinitionModel | None = None
        try:
            self.__set_generated_functions_call()
        except ValidationError:
            self.__set_default()
            return
        idx: int = 0
        if len(self.__prompts) < len(self.__generated_functions_call):
            self.__set_default()
            return
        for prompt, function_call in zip(
            self.__prompts, self.__generated_functions_call
        ):
            function_defintion = self.__get_function_definition_from_function_call(
                function_call.name
            )
            if any(
                [
                    prompt.prompt != function_call.prompt,
                    function_defintion is None
                    or not self.__is_valid_arguments(function_call, function_defintion),
                ]
            ):
                self.__set_default()
                idx = 0
                break
            idx += 1
        if idx != 0:
            self.__log_generated_function_calls()
        self.__remaining_prompts = self.__prompts[idx:]

    def __set_generated_functions_call(self) -> None:
        """Load previously generated function calls from the output JSON file.

        Reads and parses the JSON output file containing previously generated
        function calls. Raises ValidationError if the JSON is malformed.
        """
        functions_call_content: str = Path(self.__output_path).read_text()
        self.__generated_functions_call = FunctionCallRootModel.model_validate_json(
            functions_call_content
        ).root

    def __get_function_definition_from_function_call(
        self, function_call_name: str
    ) -> FunctionDefinitionModel | None:
        """Find the function definition matching a function call name.

        Searches through available definitions for one matching the given
        function name.

        Args:
            function_call_name: Name of the function to look up.

        Returns:
            FunctionDefinitionModel: Matching definition or None if not found.
        """
        for function_definition in self.__functions_definitions:
            if function_definition.name == function_call_name:
                return function_definition
        else:
            return None

    def __is_valid_arguments(
        self,
        function_call: FunctionCallModel,
        function_definition: FunctionDefinitionModel | None,
    ) -> bool:
        """Check if function call arguments match the function definition.

        Validates that all required arguments are present and have the
        correct types as specified in the function definition.

        Args:
            function_call: Generated function call to validate.
            function_definition: Function definition specifying expected args.

        Returns:
            bool: True if all arguments are valid, False otherwise.
        """
        if function_definition:
            for arg_name, arg_type in function_definition.parameters.items():
                if arg_name not in function_call.parameters.keys():
                    return False
                match arg_type.type:
                    case "string":
                        if not isinstance(function_call.parameters[arg_name], str):
                            return False
                    case "integer":
                        if not isinstance(function_call.parameters[arg_name], int):
                            return False
                    case "boolean":
                        if not isinstance(function_call.parameters[arg_name], bool):
                            return False
                    case "number":
                        if not isinstance(function_call.parameters[arg_name], float):
                            return False
                    case "float":
                        if not isinstance(function_call.parameters[arg_name], float):
                            return False
        return True

    def __set_default(self) -> None:
        """Reset the recovery state so generation starts fresh.

        Clears all recovered output and marks all prompts as remaining,
        causing the generation pipeline to start from the beginning.
        """
        self.__generated_functions_call = list()
        self.__remaining_prompts = self.__prompts

    @property
    def remaining_prompts(self) -> list[PromptModel]:
        """Get prompts that still need generation.

        Returns:
            list[PromptModel]: Remaining prompts to process.
        """
        return self.__remaining_prompts

    @property
    def generated_functions_calls(self) -> list[FunctionCallModel]:
        """Get the recovered or newly generated function-call objects.

        Returns:
            list[FunctionCallModel]: Function calls available for continuation.
        """
        return self.__generated_functions_call

    def __init_log(self) -> None:
        """Initialize log rows for each prompt before generation begins.

        Creates one log row per input prompt to track generation progress
        throughout the pipeline execution.
        """
        self.__log.add_rows(
            [LogRow(prompt.id, prompt.prompt) for prompt in self.__prompts]
        )

    def __log_generated_function_calls(self) -> None:
        """Log the recovered function calls for the current prompt batch.

        Updates log rows to display the recovered function calls and their
        corresponding function definitions in the progress table.
        """
        for prompt, function_call in zip(
            self.__prompts, self.__generated_functions_call
        ):
            function_definition: FunctionDefinitionModel | None = (
                self.__get_function_definition_from_function_call(function_call.name)
            )
            if function_definition:
                self.__log.add_row(
                    LogRow(
                        prompt.id,
                        prompt.prompt,
                        function_definition.model_dump_json(indent=4),
                        function_call.model_dump_json(indent=4),
                    )
                )
