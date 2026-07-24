from typing_extensions import Self
from src.llm.model import Model
import src.constants.constants as constants


class Cache:
    __instance: Self | None = None

    class Builder:
        def __init__(self) -> None:
            self.__model: Model
            self.__tokens_ids: dict[str, int] = dict()
            self.__function_name_static_prompt_ids: list[int]
            self.__function_arguments_static_prompt_ids: list[int]

        def build(self) -> None:
            Cache(self)

        def set_model(self, model: Model) -> Self:
            self.__model = model
            return self

        def set_tokens_ids(self) -> Self:
            def __encode_list(lst: list[str]) -> None:
                for ch in lst:
                    ch_id: int = self.__model.encode_text(ch)[0]
                    self.__tokens_ids[ch] = ch_id

            __encode_list(constants.ESCAPE_SEQUENCES)
            __encode_list(constants.NUMBERS)
            __encode_list(constants.CHAT_TEMPLATES)
            __encode_list(constants.BOOLEANS)
            return self

        def set_function_name_static_prompt(self, prompt: str) -> Self:
            self.__function_name_static_prompt_ids = self.__model.encode_text(prompt)
            return self

        def set_function_argument_static_prompt(self, prompt: str) -> Self:
            self.__function_arguments_static_prompt_ids = self.__model.encode_text(
                prompt
            )
            return self

        @property
        def function_arguments_static_prompt_ids(self) -> list[int]:
            return self.__function_arguments_static_prompt_ids.copy()

        @property
        def function_name_static_prompt_ids(self) -> list[int]:
            return self.__function_name_static_prompt_ids.copy()

        @property
        def tokens_ids(self) -> dict[str, int]:
            return self.__tokens_ids.copy()

    def __new__(cls, builder: Builder | None = None) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, builder: Builder | None = None) -> None:
        if builder:
            self.__function_name_static_prompt_ids: list[int] = (
                builder.function_name_static_prompt_ids
            )
            self.__function_arguments_static_prompt_ids: list[int] = (
                builder.function_arguments_static_prompt_ids
            )
            self.__tokens_ids = builder.tokens_ids

    @property
    def function_name_static_prompt_ids(self) -> list[int]:
        return self.__function_name_static_prompt_ids.copy()

    @property
    def function_arguments_static_prompt_ids(self) -> list[int]:
        return self.__function_arguments_static_prompt_ids.copy()

    def get_token_id(self, token: str) -> int:
        return self.__tokens_ids[token]
