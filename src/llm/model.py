"""Facade around the local language model SDK used by the pipeline."""

from typing_extensions import override
from llm_sdk.llm_sdk import Small_LLM_Model
import torch


class Model(Small_LLM_Model):
    """Wrap the small LLM SDK with convenience methods for token and logits handling."""

    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-0.6B",
        *,
        device: str | None = None,
        dtype: torch.dtype | None = None,
        trust_remote_code: bool = True,
    ) -> None:
        super().__init__(
            model_name,
            device=device,
            dtype=dtype,
            trust_remote_code=trust_remote_code,  # constructor
        )
        self.__vocab: dict[str, int]
        self.__reverse_vocab: dict[str, str]

    def encode_text(self, text: str) -> list[int]:
        """Encode a text string into token IDs.

        Args:
            text: Text to encode.

        Returns:
            list[int]: Token IDs produced by the model tokenizer.
        """
        text_ids: list[int] = [int(x) for x in super().encode(text).flatten()]
        return text_ids

    def get_logits(self, input_ids: list[int]) -> list[float]:
        """Get logits for a sequence of input token IDs.

        Args:
            input_ids: Token IDs to score.

        Returns:
            list[float]: Logits for the supplied tokens.
        """
        logits: list[float] = self.get_logits_from_input_ids(input_ids)
        return logits

    @override
    def decode(self, ids: torch.Tensor | list[int]) -> str:
        """Decode token IDs back to text.

        Args:
            ids: Token IDs or tensor containing token IDs.

        Returns:
            str: Decoded text.
        """
        return super().decode(ids)

    def get_masked_logits(
        self, text_ids: list[int], hight_score_ids: list[int]
    ) -> list[float]:
        """Mask out disallowed tokens and return the remaining logits.

        Args:
            text_ids: Token IDs used as model input.
            hight_score_ids: Allowed token IDs for the current decoding step.

        Returns:
            list[float]: Logits with illegal tokens suppressed to negative infinity.
        """
        logits: list[float] = self.get_logits(text_ids)
        if hight_score_ids:
            for idx, _ in enumerate(logits):
                if idx not in hight_score_ids:
                    logits[idx] = float("-inf")
        return logits
