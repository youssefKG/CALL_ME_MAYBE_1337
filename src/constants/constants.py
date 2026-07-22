ESCAPE_SEQUENCES: list[str] = [
    "\\",
    "'",
    '"',
    "a",
    "b",
    "f",
    "n",
    "r",
    "t",
    "v",
    "0",
    "x",
    "u",
    "U",
    "N",
    ".",
    "^",
    "$",
    "*",
    "+",
    "?",
    "{",
    "}",
    "[",
    "]",
    "(",
    ")",
    "|",
    ",",
    "i",
]

CHAT_TEMPLATES = ["<|im_end|>", "<|im-start|>", "<think>", "</think>"]

NUMBERS = [
    "-",  # negative sign
    "+",  # only valid in exponent
    ".",  # decimal point
    "e",  # exponent
    "E",  # exponent
    *list("0123456789"),
]

booleans = ["true", "false"]
