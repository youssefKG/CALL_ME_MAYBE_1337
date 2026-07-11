from collections.abc import Generator
from src.models.function_definition_model import FunctionDefinitionModel
from src.predictors.fn_name_predictor import FunctionNamePredictor
from src.LlmModel.model import Model
from src.parser.parser import Parser
from src.prompts.prompt_generator import PromptGenerator
from src.cache.cache import Cache
from .function_name_generator import FunctionNameGenerator


class OutputGenerator:
    def __init__(self, parser: Parser) -> None:
        self.__model: Model = Model()
        self.__cache = Cache()
        self.__parser: Parser = parser
        self.__prompt_generator: PromptGenerator = (
            PromptGenerator.Builder(
                self.__parser.get_fns_def, self.__parser.get_prompts
            )
            .set_params_static_prompt()
            .set_fns_def_static_prompt()
            .build()
        )
        self.__function_name_predictor: FunctionNamePredictor = FunctionNamePredictor()
        self.__init_cache()
        self.__init_functions_name_predictor()

    def generate_function_name(self) -> Generator[str | None]:
        prompt_generator: Generator[str | None] = self.__prompt_generator.next_prompt
        prompt: str | None = next(prompt_generator)
        while prompt is not None:
            fn_name_generator: FunctionNameGenerator = FunctionNameGenerator(
                self.__model,
                self.__cache,
                self.__function_name_predictor,
                self.__prompt_generator,
                prompt,
            )
            fn_name_generator.generate()
            yield fn_name_generator.fn_name
            prompt = next(prompt_generator)
        yield None

    def generate_function_param(self, function: FunctionDefinitionModel) -> None:
        pass

    def __init_cache(self) -> None:
        encoded_fns_def_names_ids: list[int] = self.__model.encode_text(
            self.__prompt_generator.get_fns_def_static_prompt
        )
        self.__cache.set_fns_def_static_prompt_ids(encoded_fns_def_names_ids)

    def __init_functions_name_predictor(self) -> None:
        fns_def_names_ids: list[list[int]] = list()
        for fn_def in self.__parser.get_fns_def:
            fns_def_names_ids.append(self.__model.encode_text(fn_def.name))
        self.__function_name_predictor.set_fns_names_ids_trie(fns_def_names_ids)
