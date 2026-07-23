from src.predictors.fn_param_predictor import (
    FunctionParametersPredictor,
    NumberState,
    StringState,
    BooleanState,
)
from src.models.function_definition_model import FunctionDefinitionModel
from src.models.functions_call import Argument
from src.LlmModel.model import Model
from src.cache.cache import Cache
from collections.abc import Generator
from src.prompts.prompt_generator import PromptGenerator
import torch
from typing import cast, Literal


class FunctionArgumentsGenerator:

    def __init__(
        self,
        prompt_generator: PromptGenerator,
        user_prompt: str,
        function_definition: FunctionDefinitionModel,
        model: Model,
        function_parameters_predictor: FunctionParametersPredictor,
    ) -> None:
        self.__prompt_generator: PromptGenerator = prompt_generator
        self.__text_ids: list[int] = list()
        self.__model: Model = model
        self.__function_arguments: Argument = dict()
        self.__user_prompt: str = user_prompt
        self.__function_definition: FunctionDefinitionModel = function_definition
        self.__cache: Cache = Cache()
        self.__function_parameters_predictor: FunctionParametersPredictor = (
            function_parameters_predictor
        )
        self.__generated_tokens: str = str()

    def generate(self) -> None:
        for arg_name, arg_type in self.__arg_iter():
            self.__generated_tokens = str()
            self.__prepare_next_argument(arg_name, arg_type)
            self.__log_text_ids()
            match arg_type:
                case "number":
                    self.__generate_number(arg_name)
                case "string":
                    self.__generate_string(arg_name)
                case "boolean":
                    self.__generate_boolean(arg_name)

    def __generate_boolean(self, arg_name: str) -> None:
        next_state: BooleanState
        possible_tokens_ids: list[int]
        while True:
            possible_tokens_ids = self.__function_parameters_predictor.next_tokens_ids(
                self.__generated_tokens, "boolean"
            )
            token, tokens_id = self.__get_next_token(possible_tokens_ids)
            next_state = cast(
                BooleanState,
                self.__function_parameters_predictor.next_state(
                    self.__generated_tokens, "boolean"
                ),
            )
            self.__generated_tokens += token
            self.__text_ids += tokens_id
            if next_state == BooleanState.FINAL:
                break
            self.__function_arguments[arg_name] = (
                True if self.__generated_tokens == "true" else False
            )

    def __generate_number(self, arg_name: str) -> None:
        next_state_for_number: NumberState
        while True:
            possible_tokens: list[int] = (
                self.__function_parameters_predictor.next_tokens_ids(
                    self.__generated_tokens, "number"
                )
            )
            token, tokens_id = self.__get_next_token(possible_tokens)
            self.__generated_tokens += token
            next_state_for_number = cast(
                NumberState,
                self.__function_parameters_predictor.next_state(
                    self.__generated_tokens, "number"
                ),
            )
            print(token, end="", flush=True)
            if next_state_for_number == NumberState.FINAL:
                self.__generated_tokens = self.__generated_tokens[:-1]
                break
            self.__text_ids += tokens_id
        self.__function_arguments[arg_name] = float(self.__generated_tokens)

    def __generate_string(self, arg_name: str) -> None:
        possible_tokens: list[int]
        string_state: StringState
        while True:
            possible_tokens = self.__function_parameters_predictor.next_tokens_ids(
                self.__generated_tokens, "string"
            )
            token, tokens_ids = self.__get_next_token(possible_tokens)
            self.__generated_tokens += token
            string_state = cast(
                StringState,
                self.__function_parameters_predictor.next_state(
                    self.__generated_tokens, "string"
                ),
            )
            print(token, end="", flush=True)
            if string_state == StringState.FINAL:
                double_quotes_ids: int = self.__generated_tokens.rindex('"')
                self.__generated_tokens = self.__generated_tokens[:double_quotes_ids]
                break
            self.__text_ids += tokens_ids
        self.__function_arguments[arg_name] = self.__generated_tokens

    def __get_next_token(self, high_score_tokens: list[int]) -> tuple[str, list[int]]:
        masked_logits: list[float] = self.__model.get_masked_logits(
            self.__text_ids, high_score_tokens
        )
        tokens_id: list[int] = cast(
            list[int], [torch.argmax(torch.tensor(masked_logits))]
        )
        token: str = self.__model.decode(torch.tensor(tokens_id[0]))
        if "\\" in token:
            token = token[: token.index("\\") + 1]
            tokens_id = self.__model.encode_text(token)
        return (token, tokens_id)

    def __set_dynamic_prompt(self, arg_name: str, arg_type: str) -> None:
        dynamic_prompt: str = self.__prompt_generator.function_argument_dynamic_prompt(
            self.__function_definition,
            self.__user_prompt,
            self.__function_arguments,
            arg_name,
            arg_type,
        )
        dynamic_prompt_ids: list[int] = self.__model.encode_text(dynamic_prompt)
        self.__text_ids += dynamic_prompt_ids

    def __set_static_prompt_ids(self) -> None:
        self.__text_ids = self.__cache.function_arguments_static_prompt_ids

    def __prepare_next_argument(
        self, arg_name: str, arg_type: Literal["boolean", "string", "number"]
    ) -> None:
        self.__set_static_prompt_ids()
        self.__set_dynamic_prompt(arg_name, arg_type)

    def __arg_iter(
        self,
    ) -> Generator[tuple[str, Literal["string", "number", "boolean"]]]:
        for arg_name, arg in self.__function_definition.parameters.items():
            yield (arg_name, arg.type)

    def __log_text_ids(self) -> None:
        for token_id in self.__text_ids:
            print(self.__model.decode(torch.tensor(token_id)), end="", flush=True)

    @property
    def function_arguments(self) -> dict[str, float | bool | str]:
        return self.__function_arguments
