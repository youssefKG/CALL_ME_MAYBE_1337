from tokenize import String

from src.cache.cache import Cache
from src.constraints.regex_constraint import RegexConstraint
from enum import Enum


class StringState(str, Enum):
    START = ""
    OPEN_CONTENT = '"'
    ESCAPE = '"\\nrtbf.*?$[]()+{}i^'
    CONTENT = "any charactere"
    CLOSED_CONTENT = ","


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
        fraction_counter: int = 0
        interger_counter: int = 0
        for ch in num:
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
                    elif interger_counter == 10:
                        current_state = NumberState.FINAL
                    else:
                        interger_counter += 1
                case NumberState.FRACTION:
                    if ch == "," or ch not in NumberState.SIGN.value:
                        current_state = NumberState.FINAL
                    elif fraction_counter == 6:
                        current_state = NumberState.FINAL
                    else:
                        fraction_counter += 1
                case NumberState.FINAL:
                    ...
        return current_state

    def next_string_possible_tokens_ids(self, string: str) -> list[int]:
        tokens_ids: list[int] = list()
        next_state: StringState = self.next_string_state(string)

        return tokens_ids

    def next_string_state(self, string: str) -> StringState:
        current_state: StringState = StringState.START
        for ch in string:
            match current_state:
                case StringState.START:
                    current_state = StringState.OPEN_CONTENT
                case StringState.OPEN_CONTENT:
                    current_state = StringState.CONTENT
                case StringState.CONTENT:
                    if ch == '"':
                        current_state = StringState.CLOSED_CONTENT
                    elif ch == "\\":
                        current_state = StringState.ESCAPE
                case StringState.ESCAPE:
                    current_state = StringState.CONTENT
                case StringState.CLOSED_CONTENT:
                    pass
        return current_state
