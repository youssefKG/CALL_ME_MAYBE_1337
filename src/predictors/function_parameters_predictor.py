"""State-machine helpers for constrained argument generation."""

from src.cache.cache import Cache
from enum import Enum
from typing import Literal


class StringState(str, Enum):
    """Define states used during constrained string generation.

    Each state determines the valid characters or tokens for the next step.
    """

    START = list('"')
    ESCAPE = list("")
    CONTENT = list("any")
    FINAL = list(",")


class NumberState(str, Enum):
    """Define states used during constrained number generation.

    The states represent the progression from the initial sign and digits
    through the optional fractional part to the final state.
    """

    START = list("-+0123456789")
    SIGN = list("0123456789")
    INTEGER = list("0123456789.,")
    FRACTION = list("0123456789,")
    FINAL = list(",")


class BooleanState(str, Enum):
    """Define states used during constrained boolean generation.

    The states restrict boolean values to the supported true and false
    representations.
    """

    START = ["true", "false"]
    FINAL = list(",")


class FunctionParametersPredictor:
    """Provide token constraints for function parameter generation.

    Uses finite-state machines to determine valid tokens for supported
    argument types during constrained decoding.
    """

    def __init__(self, *, cache: Cache) -> None:
        """Initialize the function parameter predictor.

        Args:
            cache: Cache used to retrieve token IDs.

        Returns:
            None.
        """
        self.__cache: Cache = cache

    def next_tokens_ids(
        self, content: str, arg_type: Literal["number", "string", "boolean"]
    ) -> list[int]:
        """Get valid token IDs for the next generation step.

        Args:
            content: Current generated argument content.
            arg_type: Type of the argument being generated.

        Returns:
            A list of valid token IDs.
        """
        match arg_type:
            case "number":
                return self.__next_number_tokens_ids(content)
            case "string":
                return self.__next_string_tokens_ids(content)
            case "boolean":
                return self.__next_boolean_tokens_ids(content)

    def __next_number_tokens_ids(self, num: str) -> list[int]:
        """Get valid token IDs for the next number character.

        Args:
            num: Current generated number.

        Returns:
            A list of token IDs allowed by the current number state.
        """
        next_state: NumberState = self.__number_state(num)
        return [self.__cache.get_token_id(ch) for ch in next_state.value]

    def next_state(
        self, content: str, arg_type: Literal["number", "string", "boolean"]
    ) -> NumberState | StringState | BooleanState:
        """Determine the current state for an argument.

        Args:
            content: Current generated argument content.
            arg_type: Type of the argument being generated.

        Returns:
            The state corresponding to the specified argument type.
        """
        match arg_type:
            case "number":
                return self.__number_state(content)
            case "string":
                return self.__string_state(content)
            case "boolean":
                return self.__boolean_state(content)

    def __number_state(self, num: str) -> NumberState:
        """Determine the state of a partially generated number.

        Args:
            num: Current generated number content.

        Returns:
            The current number-generation state.
        """
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
        """Determine the state of a partially generated boolean.

        Args:
            boolean_value: Current generated boolean content.

        Returns:
            The current boolean-generation state.
        """
        current_state: BooleanState = BooleanState.START
        if boolean_value:
            current_state = BooleanState.FINAL
        return current_state

    def __next_boolean_tokens_ids(self, boolean_value: str) -> list[int]:
        """Get valid token IDs for the next boolean value.

        Args:
            boolean_value: Current generated boolean content.

        Returns:
            A list of token IDs allowed by the current boolean state.
        """
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
        """Get valid token IDs for the next string character.

        Args:
            content: Current generated string content.

        Returns:
            A list of token IDs allowed by the current string state.
        """
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
        """Determine the state of a partially generated string.

        Args:
            string: Current generated string content.

        Returns:
            The current string-generation state.
        """
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
