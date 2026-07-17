from enum import Enum
from collections.abc import Callable


class NumberState(str, Enum):
    START = "-+0123456789"
    SIGN = "0123456789"
    INTEGER = "0123456789."
    FRACTION = "0123456789"
    FINAL = ","


def create_number_predictror() -> Callable[[str], NumberState]:
    next_state: NumberState = NumberState.START

    def next_possible_tokens(num: str) -> NumberState:
        nonlocal next_state
        for c in num:
            match next_state:
                case NumberState.START:
                    if c in "-+":
                        next_state = NumberState.SIGN
                        print("sign")
                    elif c in NumberState.SIGN.value:
                        next_state = NumberState.INTEGER
                        print("integer")
                case NumberState.SIGN:
                    next_state = NumberState.INTEGER
                    print("interger from sign")
                case NumberState.INTEGER:
                    if c == ",":
                        next_state = NumberState.FINAL
                        print("final")
                    elif c == ".":
                        next_state = NumberState.FRACTION
                        print("fraction")
                case NumberState.FRACTION:
                    if c not in NumberState.FRACTION:
                        next_state = NumberState.FINAL
                        print("final")
                case NumberState.FINAL:
                    ...

        return next_state

    return next_possible_tokens


def main() -> None:
    number_predictor_generator: Callable[[str], NumberState] = (
        create_number_predictror()
    )
    num: str = "-1.23"
    number_predictor: NumberState = number_predictor_generator(num)
    print(number_predictor.value)


if __name__ == "__main__":
    main()
    pass
