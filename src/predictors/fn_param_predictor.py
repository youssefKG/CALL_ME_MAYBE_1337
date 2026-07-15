from src.cache.cache import Cache
from src.constraints.regex_constraint import RegexConstraint


class FunctionParametersPredictor:
    def __init__(self, cache: Cache) -> None:
        self.__cache: Cache = cache
        self.__number_pattern: str = r"/^[+-]?\d+(?:\.\d+)?$/"
        self.__string_pattern: str = r"^[\x00-\x7F]*$"
        self.__regex_constraint: RegexConstraint = RegexConstraint()

    def next_possible_tokens_ids(self, content: str, arg_type: str) -> list[int]:
        tokens_ids: list[int] = list()
        match arg_type:
            case "number":
                return self.__regex_constraint.get_valid_tokens(
                    self.__number_pattern, content
                )
            case "string":
                return self.__regex_constraint.get_valid_tokens(
                    self.__string_pattern, content
                )
            case "bool":
                pass
            case _:
                pass
        return tokens_ids
