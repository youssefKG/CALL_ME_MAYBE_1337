from enum import Enum


class StringState(str, Enum):
    START = ""
    OPEN_CONTENT = '"'
    ESCAPE = '"\\nrtbf.*?$[]()+{}i^'
    CONTENT = "any charactere"
    CLOSED_CONTENT = ","


def next_string_state(string: str) -> StringState:
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


def main() -> None:
    string: str = f'"1\\n\\""'
    next_state: StringState = next_string_state(string)
    print(next_state.name, next_state.value)


if __name__ == "__main__":
    main()
