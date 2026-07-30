"""Facade around the local language model SDK used by the pipeline."""

from typing_extensions import override
from llm_sdk.llm_sdk import Small_LLM_Model
import torch


class Model(Small_LLM_Model):
    """Wrap the LLM SDK with methods for token and logits handling.

    Provides a simplified interface for encoding text, decoding tokens,
    retrieving logits, and applying token constraints during generation.
    """

    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-0.6B",
        *,
        device: str | None = None,
        dtype: torch.dtype | None = None,
        trust_remote_code: bool = True,
    ) -> None:
        """Initialize the language model wrapper.

        Args:
            model_name: Name or path of the language model to load.
            device: Device on which the model should run.
            dtype: Data type used by the model.
            trust_remote_code: Whether to allow execution of remote model code.

        Returns:
            None.
        """
        super().__init__(
            model_name,
            device=device,
            dtype=dtype,
            trust_remote_code=trust_remote_code,  # constructor
        )
        self.__vocab: dict[str, int]
        self.__reverse_vocab: dict[str, str]

    def encode_text(self, text: str) -> list[int]:
        """Encode text into token IDs.

        Args:
            text: Text to encode.

        Returns:
            A list of token IDs produced by the model tokenizer.
        """
        text_ids: list[int] = [int(x) for x in super().encode(text).flatten()]
        return text_ids

    def get_logits(self, input_ids: list[int]) -> list[float]:
        """Get logits produced for the given input token IDs.

        Args:
            input_ids: Token IDs used as model input.

        Returns:
            A list of logits produced by the model.
        """
        logits: list[float] = self.get_logits_from_input_ids(input_ids)
        return logits

    @override
    def decode(self, ids: torch.Tensor | list[int]) -> str:
        """Decode token IDs into text.

        Args:
            ids: Token IDs or a tensor containing token IDs.

        Returns:
            The decoded text.
        """
        return super().decode(ids)

    def get_masked_logits(
        self, text_ids: list[int], hight_score_ids: list[int]
    ) -> list[float]:
        """Return logits with disallowed tokens masked.

        Args:
            text_ids: Token IDs used as model input.
            hight_score_ids: Token IDs allowed during the current decoding step.

        Returns:
            A list of logits where disallowed token scores are negative infinity.
        """
        logits: list[float] = self.get_logits(text_ids)
        if hight_score_ids:
            for idx, _ in enumerate(logits):
                if idx not in hight_score_ids:
                    logits[idx] = float("-inf")
        return logits
