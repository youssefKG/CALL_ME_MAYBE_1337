"""Generate valid function names using constrained decoding with a trie."""

from src.predictors import FunctionNamePredictor, FunctionNameState
from src.llm import Model
from src.prompts import PromptGenerator
from src.cache.cache import Cache
import numpy as np


class FunctionNameGenerator:
    """Generate a valid function name using constrained decoding.

    The generator prepends the static and dynamic prompts, then uses the
    function-name predictor to restrict decoding to known function names.

    Attributes:
        __model: Language model used for tokenization and logits.
        __prompt_generator: Builder for prompt templates.
        __function_name_predictor: Predictor that constrains valid tokens.
        __cache: Shared cache of prompt and token IDs.
        __text_ids: Full token sequence used for decoding.
        __generated_ids: Token IDs generated for the function name.
        __function_name_tokens: Decoded tokens accumulated into the name.
        __prompt: User prompt being processed.
        __fn_name: Final generated function name.
    """

    def __init__(
        self,
        model: Model,
        /,
        *,
        cache: Cache,
        function_name_predictor: FunctionNamePredictor,
        prompt_generator: PromptGenerator,
        prompt: str,
    ) -> None:
        """Initialize the generator with model, cache, predictor, and prompt.

        Args:
            model: Language model used for tokenization and logits.
            cache: Shared cache containing static prompt token IDs.
            function_name_predictor: Predictor that restricts valid names.
            prompt_generator: Prompt builder used for the dynamic prompt.
            prompt: User prompt to convert into a function name.
        """
        self.__model = model
        self.__prompt_generator: PromptGenerator = prompt_generator
        self.__function_name_predictor: FunctionNamePredictor = (
            function_name_predictor
        )
        self.__cache: Cache = cache
        self.__text_ids: list[int] = list()
        self.__generated_ids: list[int] = list()
        self.__prompt: str = prompt
        self.__fn_name: str = ""
        self.__init_text_ids()

    def generate(self) -> None:
        """Generate the function name token by token.

        Uses the predictor to constrain next-token choices until the
        generated token sequence matches a complete known function name.
        """
        current_state: FunctionNameState
        possible_tokens_ids: list[int]
        while True:
            possible_tokens_ids = (
                self.__function_name_predictor.get_next_predictions_ids(
                    self.__generated_ids, self.__fn_name
                )
            )
            token, token_id = self.__get_next_token(possible_tokens_ids)
            self.__fn_name += token
            current_state = self.__function_name_predictor.function_name_state(
                self.__fn_name
            )
            if current_state == FunctionNameState.FINAL or (
                current_state == FunctionNameState.CONTENT
                and len(self.__fn_name) >= len(self.__prompt)
            ):
                if '"' in self.__fn_name:
                    double_quotes_idx: int = self.__fn_name.rindex('"')
                    self.__fn_name = self.__fn_name[:double_quotes_idx]
                break
            self.__text_ids.append(token_id)
            self.__generated_ids.append(token_id)

    def __get_next_token(self, high_score_ids: list[int]) -> tuple[str, int]:

        masked_logits: list[float] = self.__model.get_masked_logits(
            self.__text_ids, high_score_ids
        )
        token_id: int = int(np.argmax(masked_logits))
        token: str = self.__model.decode_ids([token_id])
        return token, token_id

    def __init_text_ids(self) -> None:
        """Initialize the token buffer with static and dynamic prompts."""
        self.__text_ids = (
            self.__cache.function_name_static_prompt_ids
            + self.__model.encode_text(
                self.__prompt_generator.function_name_dynamic_prompt(
                    self.__prompt
                )
            )
        )

    @property
    def fn_name(self) -> str:
        """Get the generated function name.

        Returns:
            str: The decoded function name.
        """
        return self.__fn_name
