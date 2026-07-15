from typing_extensions import Self
import re


class RegexConstraint:
    __instance: Self | None = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__vocab: dict[str, int]
        self.__regex_number_pattern: re.Pattern[str] = re.compile(
            r"/^[+-]?\d+(?:\.\d+)?$/"
        )
        self.__regex_string_pattern: re.Pattern[str] = re.compile(r"^[\x00-\x7F]*$")

    def get_valid_tokens(self, pattern: str, current: str) -> list[int]:
        regex = re.compile(pattern)
        valid: list[int] = []
        for token, token_id in self.__vocab.items():
            candidate = current + token
            if regex.match(candidate):
                valid.append(token_id)
        return valid

    def set_vocab(self, vocab: dict[str, int]) -> None:
        self.__vocab = dict()
        for token, token_id in vocab.items():
            if self.__regex_string_pattern.match(token):
                self.__vocab[token] = token_id
        print("clean vocab length: ", len(self.__vocab))
