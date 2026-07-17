from src.cache.cache import Cache
from src.constraints.regex_constraint import RegexConstraint
from collections.abc import Callable
from enum import Enum


class NumberState(str, Enum):
    START = "0123456789.-+"
    INTEGER = "0123456789"
    DICIMAL_POINT = "."
    FRACTION = "0123456789"
    FINAL = ","


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
                return self.__cache.get_numbers_ids
            case "string":
                return self.__regex_constraint.get_valid_tokens(
                    self.__string_pattern, content
                )
            case "bool":
                pass
            case _:
                pass
        return tokens_ids

    def create_number_predictror(self) -> Callable[[str], NumberState]:
        prev_state: NumberState = NumberState.START
        last_index: int = 0

        def next_state(num: str) -> NumberState:
            nonlocal prev_state
            nonlocal last_index
            last_index += 1
            if last_index < len(num):
                return NumberState.FINAL
            while last_index < len(num):
                pass

            return prev_state

        return next_state
