from enum import Enum, auto


class JsonState(str, Enum):
    L_BRACE = "["
    R_BRACE = "]"
    LBRACKET = "{"
    R_BRACKET = "}"
    NUMBER = auto()
    BOOL = auto()
    STRING = auto()
    OK = auto()
    QUOTE = auto()
    KEY = auto()
    NULL = auto()
    COLON = auto()
