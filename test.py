from enum import Enum


class NumberState(str, Enum):
    START = "-+0123456789"
    SIGN = "0123456789"
    INTEGER = "0123456789."
    FRACTION = "0123456789,"
    FINAL = ","


class NumPredictor:
    def __init__(self) -> None:
        self.current_state: NumberState = NumberState.START

    def next_state(self, num: str) -> None:
        for c in num:  # -1.
            match self.current_state:  # -
                case NumberState.START:
                    if c in "+-":
                        self.current_state = NumberState.SIGN
                    else:
                        self.current_state = NumberState.INTEGER
                case NumberState.SIGN:
                    self.current_state = NumberState.INTEGER
                case NumberState.INTEGER:
                    if c == ".":
                        self.current_state = NumberState.FRACTION
                case NumberState.FRACTION:
                    if c == ",":
                        self.current_state = NumberState.FINAL
                case NumberState.FINAL:
                    ...

            # current state = SIGN


def main() -> None:
    state = NumberState.SIGN
    state = NumberState.FRACTION
    print(state.name)
    number_predictor_generator: NumPredictor = NumPredictor()
    num: str = "111"
    number_predictor_generator.next_state(num)
    print(
        number_predictor_generator.current_state.value,
        number_predictor_generator.current_state.name,
    )


if __name__ == "__main__":
    main()
