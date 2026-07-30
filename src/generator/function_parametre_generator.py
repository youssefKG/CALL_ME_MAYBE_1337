from src.models.prompt_model import PromptModel
from src.predictors import (
    FunctionParametersPredictor,
    NumberState,
    StringState,
    BooleanState,
)
from typing import cast, Literal
from src.models.function_definition_model import FunctionDefinitionModel, ArgumentType
from src.log.log import Log, LogRow
from src.models import Argument
from src.llm.model import Model
from src.cache.cache import Cache
from collections.abc import Generator
from src.prompts.prompt_generator import PromptGenerator
import numpy as np


class FunctionArgumentsGenerator:

    def __init__(
        self,
        model: Model,
        /,
        *,
        cache: Cache,
        prompt_generator: PromptGenerator,
        user_prompt: PromptModel,
        function_definition: FunctionDefinitionModel,
        function_parameters_predictor: FunctionParametersPredictor,
        log: Log,
    ) -> None:
        self.__prompt_generator: PromptGenerator = prompt_generator
        self.__text_ids: list[int] = list()
        self.__model: Model = model
        self.__function_arguments: Argument = dict()
        self.__user_prompt: PromptModel = user_prompt
        self.__function_definition: FunctionDefinitionModel = function_definition
        self.__cache: Cache = cache
        self.__function_parameters_predictor: FunctionParametersPredictor = (
            function_parameters_predictor
        )
        self.__generated_tokens: str = str()
        self.__log: Log = log

    def generate(self) -> None:
        for arg_name, arg_type in self.__arg_iter():
            self.__generated_tokens = str()
            self.__prepare_next_argument(arg_name, arg_type)
            if arg_type in ("float", "number", "integer"):
                self.__generate_number(arg_name)
            elif arg_type == "string":
                self.__generate_string(arg_name)
            elif arg_type == "boolean":
                self.__generate_boolean(arg_name)
            self.__set_argument(arg_name, arg_type, self.__generated_tokens)

    def __set_argument(
        self,
        arg_name: str,
        arg_type: ArgumentType,
        arg_value: str,
    ) -> None:
        match arg_type:
            case "number":
                self.__function_arguments[arg_name] = float(arg_value)
            case "float":
                self.__function_arguments[arg_name] = float(arg_value)
            case "integer":
                self.__function_arguments[arg_name] = int(arg_value)
            case "string":
                self.__function_arguments[arg_name] = arg_value
            case "boolean":
                self.__function_arguments[arg_name] = (
                    True if arg_value == "true" else False
                )

    def __generate_boolean(self, arg_name: str) -> None:
        next_state: BooleanState
        possible_tokens_ids: list[int]
        while True:
            possible_tokens_ids = self.__function_parameters_predictor.next_tokens_ids(
                self.__generated_tokens, "boolean"
            )
            token, token_id = self.__get_next_token(possible_tokens_ids)
            next_state = cast(
                BooleanState,
                self.__function_parameters_predictor.next_state(
                    self.__generated_tokens, "boolean"
                ),
            )
            if next_state == BooleanState.FINAL:
                break
            self.__generated_tokens += token
            self.__text_ids.append(token_id)
            self.__log_params(arg_name, "boolean")

    def __generate_number(self, arg_name: str) -> None:
        current_state: NumberState
        while True:
            possible_tokens: list[int] = (
                self.__function_parameters_predictor.next_tokens_ids(
                    self.__generated_tokens, "number"
                )
            )
            token, token_id = self.__get_next_token(possible_tokens)
            self.__generated_tokens += token
            current_state = cast(
                NumberState,
                self.__function_parameters_predictor.next_state(
                    self.__generated_tokens, "number"
                ),
            )
            if current_state == NumberState.FINAL:
                if "," in self.__generated_tokens:
                    semi_column_idx: int = self.__generated_tokens.rindex(",")
                    self.__generated_tokens = self.__generated_tokens[:semi_column_idx]
                break
            self.__text_ids.append(token_id)
            self.__log_params(
                arg_name,
                "number",
            )

    def __generate_string(self, arg_name: str) -> None:
        possible_tokens: list[int]
        current_state: StringState
        while True:
            possible_tokens = self.__function_parameters_predictor.next_tokens_ids(
                self.__generated_tokens, "string"
            )
            token, token_id = self.__get_next_token(possible_tokens)
            self.__generated_tokens += token
            current_state = cast(
                StringState,
                self.__function_parameters_predictor.next_state(
                    self.__generated_tokens, "string"
                ),
            )
            if current_state == StringState.FINAL or (
                current_state == StringState.CONTENT
                and len(self.__generated_tokens) >= len(self.__user_prompt.prompt)
            ):
                if '"' in self.__generated_tokens:
                    double_quotes_ids: int = self.__generated_tokens.rindex('"')
                    self.__generated_tokens = self.__generated_tokens[
                        :double_quotes_ids
                    ]
                break
            self.__text_ids.append(token_id)
            self.__log_params(arg_name, "string")

    def __get_next_token(self, high_score_tokens: list[int]) -> tuple[str, int]:
        masked_logits: list[float] = self.__model.get_masked_logits(
            self.__text_ids, high_score_tokens
        )
        token_id: int = cast(int, np.argmax(masked_logits))
        token: str = self.__model.decode([token_id])
        return (token, token_id)

    def __prepare_next_argument(self, arg_name: str, arg_type: ArgumentType) -> None:
        self.__text_ids = self.__cache.function_arguments_static_prompt_ids
        dynamic_prompt: str = self.__prompt_generator.function_argument_dynamic_prompt(
            self.__function_definition,
            self.__user_prompt.prompt,
            self.__function_arguments,
            arg_name,
            arg_type,
        )
        dynamic_prompt_ids: list[int] = self.__model.encode_text(dynamic_prompt)
        self.__text_ids += dynamic_prompt_ids

    def __arg_iter(
        self,
    ) -> Generator[tuple[str, ArgumentType]]:
        for arg_name, arg in self.__function_definition.parameters.items():
            yield (arg_name, arg.type)

    def __log_params(
        self,
        arg_name: str,
        arg_type: Literal["string", "number", "boolean"],
    ) -> None:
        self.__log.add_row(
            row=LogRow(
                id=self.__user_prompt.id,
                prompt=self.__user_prompt.prompt,
                function_defintion=self.__function_definition.model_dump_json(indent=4),
                function_call=self.__prompt_generator.function_call_prompt(
                    self.__user_prompt.prompt,
                    self.__function_definition,
                    self.__function_arguments,
                    arg_name,
                    arg_type,
                )
                + self.__generated_tokens,
            ),
            status=f"{self.__user_prompt.id}-Generating argument {arg_name}",
        )

    @property
    def function_arguments(self) -> dict[str, float | bool | str]:
        return self.__function_arguments
