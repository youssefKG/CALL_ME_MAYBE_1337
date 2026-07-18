from collections.abc import Generator
from src.predictors.fn_param_predictor import FunctionParametersPredictor
from src.models.function_definition_model import FunctionDefinitionModel
from src.predictors.fn_name_predictor import FunctionNamePredictor
from src.LlmModel.model import Model
from src.parser.parser import Parser
from src.prompts.prompt_generator import PromptGenerator
from src.cache.cache import Cache
from src.utils.function import FunctionCall
from src.constraints.regex_constraint import RegexConstraint
from .function_name_generator import FunctionNameGenerator
from .function_parametre_generator import FunctionArgumentsGenerator
import src.constants.constants as constants
import json


class OutputGenerator:
    def __init__(self, parser: Parser) -> None:
        self.__parser: Parser = parser
        self.__model: Model = Model()
        self.__cache = Cache()
        self.__prompt_generator: PromptGenerator = (
            PromptGenerator.Builder(
                self.__parser.get_functions_definition, self.__parser.get_prompts
            )
            .set_params_static_prompt()
            .set_fns_def_static_prompt()
            .build()
        )
        self.__function_calls: list[FunctionCall] = list()
        self.__parsed_vocab: dict[str, int] = dict()

        self.__function_name_predictor: FunctionNamePredictor
        self.__function_parameters_predictor: FunctionParametersPredictor = (
            FunctionParametersPredictor(self.__cache)
        )
        self.__init_regex_constraint()
        self.__init_cache()
        self.__init_functions_name_predictor()
        self.__init_function_prameteres_predictor()

    def generate(self) -> Generator[FunctionCall | None]:
        prompt_generator: Generator[str | None] = self.__prompt_generator.next_prompt
        prompt: str | None = next(prompt_generator)
        while prompt:
            fn_name_generator: FunctionNameGenerator = FunctionNameGenerator(
                self.__model,
                self.__cache,
                self.__function_name_predictor,
                self.__prompt_generator,
                prompt,
            )
            fn_name_generator.generate()
            function_definition: FunctionDefinitionModel | None = (
                self.__get_function_definition(fn_name_generator.fn_name)
            )
            function_call: FunctionCall = FunctionCall(fn_name_generator.fn_name)
            if function_definition:
                function_arguments_generator: FunctionArgumentsGenerator = (
                    FunctionArgumentsGenerator(
                        prompt_generator=self.__prompt_generator,
                        user_prompt=prompt,
                        function_definition=function_definition,
                        model=self.__model,
                        cache=self.__cache,
                        function_parameters_predictor=self.__function_parameters_predictor,
                    )
                )
                function_arguments_generator.generate()
            self.__function_calls.append(function_call)
            yield FunctionCall(fn_name_generator.fn_name)
            prompt = next(prompt_generator)
        yield None

    def __get_function_definition(
        self, function_name: str
    ) -> FunctionDefinitionModel | None:
        for function_def in self.__parser.get_functions_definition:
            if function_def.name == function_name:
                return function_def
        return None

    def __init_function_prameteres_predictor(self) -> None:
        self.__function_parameters_predictor = FunctionParametersPredictor(self.__cache)

    def __init_functions_name_predictor(self) -> None:
        self.__function_name_predictor = FunctionNamePredictor()
        fns_def_names_ids: list[list[int]] = list()
        for fn_def in self.__parser.get_functions_definition:
            fns_def_names_ids.append(self.__model.encode_text(fn_def.name))
        self.__function_name_predictor.set_fns_names_ids_trie(fns_def_names_ids)

    def __init_cache(self) -> None:

        def __set_ascii_code_to_cache() -> None:
            ascii_ids: list[int] = list()
            for ascci_char in constants.ASCII:
                ascii_ids += self.__model.encode_text(ascci_char)
            self.__cache.set_ascii_ids(ascii_ids)

        def __set_numbers_ids_to_cache() -> None:
            tokens: str = "0-1234567+8,9."
            res: list[int] = []

            for t in tokens:
                token_id: int = self.__model.encode_text(t)[0]
                self.__cache.add_token(t, token_id)
            self.__cache.set_numbers_ids(res)

        encoded_fns_def_names_ids: list[int] = self.__model.encode_text(
            self.__prompt_generator.get_fns_def_static_prompt
        )
        function_argument_static_prompt_ids: list[int] = self.__model.encode_text(
            self.__prompt_generator.get_function_argument_static_prompt
        )
        im_end_id: int = self.__model.encode_text("<|im_end|>")[0]
        self.__cache.set_fns_def_static_prompt_ids(encoded_fns_def_names_ids)
        self.__cache.set_function_argument_static_prompt_ids(
            function_argument_static_prompt_ids
        )
        self.__cache.set_im_end_id(im_end_id)
        __set_numbers_ids_to_cache()
        __set_ascii_code_to_cache()

    def __init_regex_constraint(self):
        vocab_path: str = self.__model.get_path_to_vocab_file()
        vocab: dict[str, int]
        with open(vocab_path, "r") as vocab_file:
            vocab = json.loads(vocab_file.read())
        for token, token_id in vocab.items():
            clean_token = token.replace("Ġ", "").replace("Ċ", "\n")
            self.__parsed_vocab[clean_token] = token_id
        regex_constraint: RegexConstraint = RegexConstraint()
        regex_constraint.set_vocab(self.__parsed_vocab)
