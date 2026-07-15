from transformers import LayoutLMModel

from src.predictors.fn_param_predictor import FunctionParametersPredictor
from src.models.function_definition_model import FunctionDefinitionModel
from src.LlmModel.model import Model
from src.cache.cache import Cache
from collections.abc import Generator
from src.prompts.prompt_generator import PromptGenerator
import torch
from src.utils.function import FunctionParameter


class FunctionArgumentsGenerator:

    def __init__(
        self,
        prompt_generator: PromptGenerator,
        user_prompt: str,
        function_definition: FunctionDefinitionModel,
        model: Model,
        cache: Cache,
        function_parameters_predictor: FunctionParametersPredictor,
    ) -> None:

        self.__prompt_generator: PromptGenerator = prompt_generator
        self.__text_ids: list[int] = list()
        self.__model: Model = model
        self.__generated_arguments: list[FunctionParameter] = list()
        self.__user_prompt: str = user_prompt
        self.__function_definition: FunctionDefinitionModel = function_definition
        self.__cache: Cache = cache
        self.__function_parameters_predictor: FunctionParametersPredictor = (
            function_parameters_predictor
        )

    def generate(self) -> None:
        arg_generator: Generator[tuple[str, str] | None] = (
            self.__next_argument_generator()
        )
        argument: tuple[str, str] | None = next(arg_generator)
        while argument:
            arg_name, arg_type = argument
            self.__prepare_next_argument(arg_name, arg_type)
            match arg_type:
                case "number":
                    self.__generate_param_number(arg_name)
                case "string":
                    self.__generate_string(arg_name)
                case _:
                    pass
            argument = next(arg_generator)

    def __generate_param_number(self, arg_name: str) -> str:
        generated_ids: list[int] = list()
        generated_tokens: str = str()
        while True:
            possible_tokens: list[int] = (
                self.__function_parameters_predictor.next_possible_tokens_ids(
                    generated_tokens, "number"
                )
            )
            logits: list[float] = self.__model.get_masked_logits(
                self.__text_ids, possible_tokens
            )
            high_score_id = int(torch.argmax(torch.tensor(logits)))
            if high_score_id == self.__cache.im_end_id or generated_tokens.endswith(
                "0" * 3
            ):
                break
            token: str = self.__model.decode(torch.tensor(high_score_id))
            print(token)
            generated_tokens += token
            generated_ids.append(int(high_score_id))
            self.__text_ids.append(int(high_score_id))
        generated_arg_value: str = str(float(generated_tokens))
        self.__generated_arguments.append(
            FunctionParameter(arg_name, generated_arg_value)
        )
        return generated_arg_value

    def __generate_string(self, arg_name: str) -> None:
        generated_ids: list[int] = list()
        generated_tokens: str = str()
        i: int = 0
        while True and i < 30:
            """
            possible_tokens_ids: list[int] = (
                self.__function_parameters_predictor.next_possible_tokens_ids(
                    generated_tokens, "string"
                )
            )
            """
            logits: list[float] = self.__model.get_logits(self.__text_ids)
            high_score_id: int = int(torch.argmax(torch.tensor(logits)))
            if high_score_id == self.__cache.im_end_id or high_score_id == 151664:
                break

            print(high_score_id)
            token: str = self.__model.decode(torch.tensor(high_score_id))
            print("generated token: ", token)
            if token and (
                token[-1].strip() == '"'
                or token[-1].strip() == "}"
                or token[-1].strip() == ","
                or token[-1].strip().isspace()
            ):
                break
            generated_tokens += token
            generated_ids.append(high_score_id)
            self.__text_ids.append(high_score_id)
            # print(token, end="", flush=True)
            i += 1
        self.__generated_arguments.append(FunctionParameter(arg_name, generated_tokens))

    def __set_dynamic_prompt(self, arg_name: str, arg_type: str) -> None:
        dynamic_prompt: str = (
            self.__prompt_generator.get_function_arguments_dynamic_prompt(
                self.__function_definition,
                self.__user_prompt,
                self.__generated_arguments,
                arg_name,
                arg_type,
            )
        )
        # print(dynamic_prompt)
        dynamic_prompt_ids: list[int] = self.__model.encode_text(dynamic_prompt)
        # print(dynamic_prompt, end="", flush=True)
        self.__text_ids += dynamic_prompt_ids

    def __set_static_prompt_ids(self) -> None:
        self.__text_ids = self.__cache.get_function_argument_static_prompt_ids

    def __next_argument_generator(self) -> Generator[tuple[str, str] | None]:
        for arg_name, arg in self.__function_definition.parameters.items():
            yield (arg_name, arg.type)
        yield None

    def __prepare_next_argument(self, arg_name: str, arg_type: str) -> None:
        self.__set_static_prompt_ids()
        self.__set_dynamic_prompt(arg_name, arg_type)
