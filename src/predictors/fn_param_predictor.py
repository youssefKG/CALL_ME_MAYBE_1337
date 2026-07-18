from src.cache.cache import Cache
from src.constraints.regex_constraint import RegexConstraint
from enum import Enum


class NumberState(str, Enum):
    START = "-+0123456789"
    SIGN = "0123456789"
    INTEGER = "0123456789."
    FRACTION = "0123456789,"
    FINAL = ","


class FunctionParametersPredictor:
    def __init__(self, cache: Cache) -> None:
        self.__cache: Cache = cache
        self.__string_pattern: str = r"^[\x00-\x7F]*$"

    def next_possible_tokens_ids(self, content: str, arg_type: str) -> list[int]:
        tokens_ids: list[int] = list()
        match arg_type:
            case "number":
                return self.next_possible_tokens(content)
            case "string":
                return []
            case "bool":
                pass
            case _:
                pass
        return tokens_ids

    def next_possible_tokens(self, num: str) -> list[int]:
        tokens_ids: list[int] = list()
        next_state: NumberState = self.next_state_for_number(num)
        for ch in next_state.value:
            tokens_ids.append(self.__cache.get_token_id(ch))

        return tokens_ids

    def next_state_for_number(self, num: str) -> NumberState:
        current_state: NumberState = NumberState.START
        for idx, ch in enumerate(num):
            match current_state:
                case NumberState.START:
                    if ch in "-+":
                        current_state = NumberState.SIGN
                    else:
                        current_state = NumberState.INTEGER
                case NumberState.SIGN:
                    current_state = NumberState.INTEGER
                case NumberState.INTEGER:
                    if ch == ".":
                        current_state = NumberState.FRACTION
                    elif idx == 10:
                        current_state = NumberState.FINAL
                case NumberState.FRACTION:
                    if ch == "," or ch not in NumberState.SIGN.value:
                        current_state = NumberState.FINAL
                    elif idx > 4:
                        current_state = NumberState.FINAL
                case NumberState.FINAL:
                    ...
        return current_state
