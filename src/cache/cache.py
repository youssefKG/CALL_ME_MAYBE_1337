"""Cache token IDs and static prompt IDs for repeated decoding steps."""

from typing_extensions import Self
from src.llm import Model
import src.constants as constants


class Cache:
    """Singleton cache for token IDs and prompt
    prefixes used during generation.
    """

    __instance: Self | None = None

    class Builder:
        """Fluent builder for populating
        the cache with model-dependent values."""

        def __init__(self) -> None:
            """Initialize the builder with empty state.

            Attributes:
                __model: Language model for tokenization.
                __tokens_ids: Mapping of token strings to token IDs.
                __fn_name_prompt_ids: Encoded function-name prompt.
                __arg_prompt_ids: Encoded argument prompt.
            """
            self.__model: Model
            self.__tokens_ids: dict[str, int] = dict()
            self.__function_name_static_prompt_ids: list[int]
            self.__function_arguments_static_prompt_ids: list[int]

        def build(self) -> "Cache":
            """Create the singleton cache instance from the builder state.

            Returns:
                Cache: The singleton cache instance populated with values.
            """
            return Cache(self)

        def set_model(self, model: Model) -> Self:
            """Store the model used to compute token IDs.

            Args:
                model: Model instance used for tokenization.

            Returns:
                Self: The builder instance.
            """
            self.__model = model
            return self

        def set_tokens_ids(self) -> Self:
            """Populate the cache with token IDs for decoding symbols.

            Encodes all escape sequences, numbers, chat templates, and
            boolean literals using the model tokenizer.

            Returns:
                Self: The builder instance for method chaining.
            """

            def __encode_list(lst: list[str]) -> None:
                """Encode a list of strings and store their token IDs.

                Args:
                    lst: List of strings to tokenize.
                """
                for ch in lst:
                    ch_id: int = self.__model.encode_text(ch)[0]
                    self.__tokens_ids[ch] = ch_id

            __encode_list(constants.ESCAPE_SEQUENCES)
            __encode_list(constants.NUMBERS)
            __encode_list(constants.CHAT_TEMPLATES)
            __encode_list(constants.BOOLEANS)
            __encode_list(constants.OTHERS)
            return self

        def set_function_name_static_prompt(self, prompt: str) -> Self:
            """Store the function-name static prompt token IDs.

            Encodes the static prompt used for function-name generation
            and caches the resulting token sequence.

            Args:
                prompt: Static function-name prompt text.

            Returns:
                Self: The builder instance for method chaining.
            """
            prompt_ids = self.__model.encode_text(prompt)
            self.__function_name_static_prompt_ids = prompt_ids
            return self

        def set_function_argument_static_prompt(self, prompt: str) -> Self:
            """Store the function-argument static prompt token IDs.

            Encodes the static prompt used for argument generation and
            caches the resulting token sequence.

            Args:
                prompt: Static argument-generation prompt text.

            Returns:
                Self: The builder instance for method chaining.
            """
            prompt_ids = self.__model.encode_text(prompt)
            self.__function_arguments_static_prompt_ids = prompt_ids
            return self

        @property
        def function_arguments_static_prompt_ids(self) -> list[int]:
            """Get a copy of the function-argument prompt token IDs.

            Returns:
                list[int]: Argument prompt token IDs.
            """
            return self.__function_arguments_static_prompt_ids.copy()

        @property
        def function_name_static_prompt_ids(self) -> list[int]:
            """Get a copy of the function-name prompt token IDs.

            Returns:
                list[int]: Function-name prompt token IDs.
            """
            return self.__function_name_static_prompt_ids.copy()

        @property
        def tokens_ids(self) -> dict[str, int]:
            """Get a copy of the cached token ID mapping.

            Returns:
                dict[str, int]: Token string to token ID mapping.
            """
            return self.__tokens_ids.copy()

    def __new__(cls, builder: Builder | None = None) -> Self:
        """Create or return the singleton cache instance.

        Implements the singleton pattern to ensure only one cache instance
        exists per process.

        Args:
            builder: Optional builder instance for initialization.

        Returns:
            Self: The singleton cache instance.
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance

    def __init__(self, builder: Builder | None = None) -> None:
        """Initialize the cache from a builder when it is first populated."""
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
        """Get a copy of the cached static prompt token IDs."""
        return self.__function_name_static_prompt_ids.copy()

    @property
    def function_arguments_static_prompt_ids(self) -> list[int]:
        """Get a copy of the cached argument-prompt token IDs."""
        return self.__function_arguments_static_prompt_ids.copy()

    def get_token_id(self, token: str) -> int:
        """Retrieve the cached token ID for a single token string.

        Args:
            token: Token to resolve.

        Returns:
            int: Cached token identifier.
        """
        return self.__tokens_ids[token]
