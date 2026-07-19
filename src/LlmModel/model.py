from typing_extensions import override
from llm_sdk.llm_sdk import Small_LLM_Model
import torch


class Model(Small_LLM_Model):

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
        self.get_vocab()

    def encode_text(self, text: str) -> list[int]:
        text_ids: list[int] = [int(x) for x in super().encode(text).flatten()]
        return text_ids

    def get_logits(self, input_ids: list[int]) -> list[float]:
        logits: list[float] = self.get_logits_from_input_ids(input_ids)
        return logits

    @override
    def decode(self, ids: torch.Tensor | list[int]) -> str:
        return super().decode(ids)

    def get_masked_logits(
        self, text_ids: list[int], hight_score_ids: list[int]
    ) -> list[float]:
        logits: list[float] = self.get_logits_from_input_ids(text_ids)
        if hight_score_ids:
            for idx, _ in enumerate(logits):
                if idx not in hight_score_ids:
                    logits[idx] = float("-inf")
        return logits

    def get_vocab(self) -> None:
        print(self.get_path_to_vocab_file())
