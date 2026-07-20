from enum import Enum


class StringState(str, Enum):
    START = '"'
    ESCAPE = '"\\nrtbf.*?$[]()+{}i^'
    CONTENT = "any"
    FINAL = ","


def next_string_state(string: str) -> StringState:
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


def format_token(token: str) -> str:
    formatted_token: str = token
    if "\\" in token:
        formatted_token = formatted_token[: formatted_token.index("\\") + 1]
    return formatted_token


def main() -> None:
    string: str = f'"1\\n\\'
    token = "amine\\"
    formatted_token: str = format_token(token)
    next_state: StringState = next_string_state(string)
    print(next_state.name, next_state.value)
    print(formatted_token)


if __name__ == "__main__":
    main()
