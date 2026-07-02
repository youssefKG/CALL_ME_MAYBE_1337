from LlmModel.model import Model
from src.Parser.Parser import Parser
from src.prompts.prompt_generator import PromptGenerator
from src.cache.cache import Cache


class Generator:
    def __init__(self, parser: Parser) -> None:
        self.__model = Model()
        self.__cache = Cache()
        self.parser: Parser = parser
        self.__prompt_generator = PromptGenerator(parser.get_prompts)

    def __init_cache(self) -> None:
        encoded_fn_names_ids: list[int] = self.__model.encode()
        encoded_fn_params_ids: list[int] = self.__model.encode()
