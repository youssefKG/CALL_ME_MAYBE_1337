from enum import Enum


class StringState(str, Enum):
    START = '"'
    OPEN_CONTENT = "any char"
    OPEN_ESCAPE = "\\"
    CLOSED_ESCAPE = '"\\nrtbf'
    CLOSED_CONTENT = '"'
    FINISH = ","


def get_next_state(content: str) -> StringState:
    current_state: StringState = StringState.START

    for idx, ch in enumerate(content):
        match current_state:
            case StringState.START:
                if ch == "\\":
                    current_state = StringState.OPEN_ESCAPE
                elif ch == '"':
                    pass
                else:
                    current_state = StringState.OPEN_CONTENT
            case StringState.OPEN_ESCAPE:
                current_state = StringState.CLOSED_ESCAPE
            case StringState.CLOSED_ESCAPE:
                current_state = StringState.OPEN_CONTENT
            case StringState.OPEN_CONTENT:
                if ch == '"':
                    current_state = StringState.CLOSED_CONTENT
                if ch == "\\":
                    current_state = StringState.OPEN_ESCAPE
            case StringState.CLOSED_CONTENT:
                current_state = StringState.FINISH
            case _:
                pass

    return current_state


def main() -> None:
    pass
