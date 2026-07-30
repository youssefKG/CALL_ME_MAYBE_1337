"""Generate valid function names using constrained decoding with a trie."""

from src.predictors import FunctionNamePredictor
from src.llm.model import Model
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
        self.__function_name_predictor: FunctionNamePredictor = function_name_predictor
        self.__cache: Cache = cache
        self.__text_ids: list[int] = list()
        self.__generated_ids: list[int] = list()
        self.__function_name_tokens: list[str] = list()
        self.__prompt: str = prompt
        self.__fn_name: str = ""
        self.__init_text_ids()

    def generate(self) -> None:
        """Generate the function name token by token.

        Uses the predictor to constrain next-token choices until the
        generated token sequence matches a complete known function name.
        """
        while True:
            self.__predict_next_token()
            if self.__function_name_predictor.is_completed(self.__generated_ids):
                break
            possible_tokens_ids: list[int] = (
                self.__function_name_predictor.get_next_predictions_ids(
                    self.__generated_ids
                )
            )
            logits: list[float] = self.__model.get_masked_logits(
                self.__text_ids, possible_tokens_ids
            )
            high_score = np.argmax(logits)
            self.__add_next_token_id(int(high_score))
        self.__fn_name = "".join(self.__function_name_tokens)

    def __add_next_token_id(self, id: int) -> None:
        """Append a generated token ID and its decoded token text.

        Args:
            id: Token ID selected by the decoder.
        """
        self.__generated_ids.append(id)
        self.__text_ids.append(id)
        token: str = self.__model.decode([id])
        self.__function_name_tokens.append(token)

    def __init_text_ids(self) -> None:
        """Initialize the token buffer with static and dynamic prompts."""
        self.__text_ids = (
            self.__cache.function_name_static_prompt_ids
            + self.__model.encode_text(
                self.__prompt_generator.function_name_dynamic_prompt(self.__prompt)
            )
        )

    def __predict_next_token(self) -> None:
        """Consume any forced tokens until a branching prediction is needed."""
        next_predicted_ids: list[int] = (
            self.__function_name_predictor.get_next_predictions_ids(
                self.__generated_ids
            )
        )
        while len(next_predicted_ids) == 1:
            next_token_id: int = next_predicted_ids[0]
            self.__add_next_token_id(next_token_id)
            next_predicted_ids = (
                self.__function_name_predictor.get_next_predictions_ids(
                    self.__generated_ids
                )
            )

    @property
    def fn_name(self) -> str:
        """Get the generated function name.

        Returns:
            str: The decoded function name.
        """
        return self.__fn_name
