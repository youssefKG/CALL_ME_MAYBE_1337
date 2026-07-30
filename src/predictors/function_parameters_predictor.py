"""State-machine helpers for constrained argument generation."""

from src.cache.cache import Cache
from enum import Enum
from typing import Literal


class StringState(list[str], Enum):
    """Possible states while generating a string argument."""

    START = list('"')
    ESCAPE = list("")
    CONTENT = list("any")
    FINAL = list(",")


class NumberState(list[str], Enum):
    """Possible states while generating a numeric argument."""

    START = list("-+0123456789")
    SIGN = list("0123456789")
    INTEGER = list("0123456789.,")
    FRACTION = list("0123456789,")
    FINAL = list(",")


class BooleanState(list[str], Enum):
    """Possible states while generating a boolean argument."""

    START = ["true", "false"]
    FINAL = list(",")


class FunctionParametersPredictor:
    """Provide next-token constraints for string, number, and boolean arguments."""

    def __init__(self, *, cache: Cache) -> None:
        self.__cache: Cache = cache

    def next_tokens_ids(
        self, content: str, arg_type: Literal["number", "string", "boolean"]
    ) -> list[int]:
        """Get the allowed next-token IDs for the current argument state.

        Args:
            content: Current partial argument content.
            arg_type: The expected argument type.

        Returns:
            list[int]: Allowed token IDs for the next decoding step.
        """
        match arg_type:
            case "number":
                return self.__next_number_tokens_ids(content)
            case "string":
                return self.__next_string_tokens_ids(content)
            case "boolean":
                return self.__next_boolean_tokens_ids(content)

    def __next_number_tokens_ids(self, num: str) -> list[int]:
        """Return allowed tokens for the next numeric-character step."""
        next_state: NumberState = self.__number_state(num)
        return [self.__cache.get_token_id(ch) for ch in next_state.value]

    def next_state(
        self, content: str, arg_type: Literal["number", "string", "boolean"]
    ) -> NumberState | StringState | BooleanState:
        """Compute the next state for a partial argument value.

        Args:
            content: Current partial argument content.
            arg_type: The expected argument type.

        Returns:
            NumberState | StringState | BooleanState: The updated state.
        """
        match arg_type:
            case "number":
                return self.__number_state(content)
            case "string":
                return self.__string_state(content)
            case "boolean":
                return self.__boolean_state(content)

    def __number_state(self, num: str) -> NumberState:
        """Determine the numeric state from the current partial number content."""
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
                    elif ch == ",":
                        current_state = NumberState.FINAL
                    elif interger_counter == 10:
                        current_state = NumberState.FINAL
                    else:
                        interger_counter += 1
                case NumberState.FRACTION:
                    if ch == "," or ch not in NumberState.SIGN.value:
                        current_state = NumberState.FINAL
                    elif fraction_counter == 10:
                        current_state = NumberState.FINAL
                    else:
                        fraction_counter += 1
                case NumberState.FINAL:
                    ...
        return current_state

    def __boolean_state(self, boolean_value: str) -> BooleanState:
        """Determine the boolean state from the current partial text."""
        current_state: BooleanState = BooleanState.START
        if boolean_value:
            current_state = BooleanState.FINAL
        return current_state

    def __next_boolean_tokens_ids(self, boolean_value: str) -> list[int]:
        """Return allowed tokens for the next boolean step."""
        current_state = self.__boolean_state(boolean_value)
        match current_state:
            case BooleanState.START:
                return [
                    self.__cache.get_token_id("true"),
                    self.__cache.get_token_id("false"),
                ]
            case _:
                return list()

    def __next_string_tokens_ids(self, content: str) -> list[int]:
        """Return allowed tokens for the next string-character step."""
        current_state: StringState = self.__string_state(content)

        match current_state:
            case StringState.START:
                return list()
            case StringState.ESCAPE:
                return [
                    self.__cache.get_token_id(token)
                    for token in StringState.ESCAPE.value
                ]
            case StringState.FINAL:
                return [self.__cache.get_token_id(",")]
            case StringState.CONTENT:
                return list()

    def __string_state(self, string: str) -> StringState:
        """Determine the string state from the current partial content."""
        current_state: StringState = StringState.START
        for ch in string:
            match current_state:
                case StringState.START:
                    current_state = StringState.CONTENT
                case StringState.CONTENT:
                    if ch == '"':
                        current_state = StringState.FINAL
                    elif ch == "\\":
                        current_state = StringState.ESCAPE
                case StringState.ESCAPE:
                    current_state = StringState.CONTENT
                case StringState.FINAL:
                    ...
        return current_state
