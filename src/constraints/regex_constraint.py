from typing_extensions import Self
import re


class RegexConstraint:
    __instance: Self | None = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self):
        self.__vocab: dict[str, int] = dict()
        self.__regex_number_pattern: re.Pattern[str] = re.compile(
            r"/^[+-]?\d+(?:\.\d+)?$/"
        )
        self.__regex_string_pattern: re.Pattern[str] = re.compile(r"^[\x00-\x7F]*$")
        self.__strings_ids: list[float] = list()

    def get_valid_tokens(self, pattern: str, current: str) -> list[int]:
        return list(self.__vocab.values())

    def set_vocab(self, vocab: dict[str, int]) -> None:
        for token, token_id in vocab.items():
            if self.__regex_string_pattern.match(token):
                self.__vocab[token] = token_id
        print("clean vocab length: ", len(self.__vocab))
