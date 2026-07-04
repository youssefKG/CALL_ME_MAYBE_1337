from src.LlmModel.model import Model
from src.Parser.Parser import Parser
from src.prompts.prompt_generator import PromptGenerator
from src.cache.cache import Cache


class Generator:
    def __init__(self, parser: Parser) -> None:
        self.__model: Model = Model()
        self.__cache = Cache()
        self.__parser: Parser = parser
        self.__prompt_generator: PromptGenerator = (
            PromptGenerator.Builder(
                self.__parser.get_fns_def, self.__parser.get_prompts
            )
            .set_params_static_prompt()
            .set_static_fns_def_static_prompt()
            .build()
        )

    def init_cache(self) -> None:
        encoded_fns_def_names_ids: list[int] = self.__model.my_encode(
            self.__prompt_generator.get_fn_params_static_prompt
        )
        encoded_fn_def_params_ids: list[int] = self.__model.my_encode(
            self.__prompt_generator.get_fn_params_static_prompt
        )
        self.__cache.set_fns_def_static_prompt_ids(encoded_fns_def_names_ids)
        self.__cache.set_fn_params_static_prompt_ids(encoded_fn_def_params_ids)
