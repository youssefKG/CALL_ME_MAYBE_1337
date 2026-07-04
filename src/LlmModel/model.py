from typing_extensions import override
from llm_sdk.llm_sdk import Small_LLM_Model
from src.utils.singleton import Singleton
import torch

#     # data_ids: list[int] = [int(x) for x in self.encode(prompt).flatten()]
#     # logits: list[float] = self.get_logits_from_input_ids(data_ids)
#     # prob_ids = torch.argmax(torch.tensor(logits), dim=-1).item()
#     # next_token: str = self.decode(torch.tensor(prob_ids))
#     next_token: str = ""


class Model(Singleton, Small_LLM_Model):

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

    def my_encode(self, text: str) -> list[int]:
        text_ids: list[int] = [int(x) for x in self.encode(text).flatten()]
        return text_ids

    def get_logits(self, input_ids: list[int]) -> list[float]:
        logits: list[float] = self.get_logits_from_input_ids(input_ids)
        return logits


#
# def get_next_token(self, prompt: str, next_preditect_token: set[str]) -> str:
#     return next_token
#
# def next_valid_token(self, current_text: str) -> set[str]:
#     valid_tokens: set[str] = set()
#
#     if not current_text:
#         return {"{"}
#
#     last_character: str = current_text[-1]
#     if last_character.isdigit():
#         return {"0", "1", "3", "4", "5", "6", "7", "8", "9"}
#
#     return valid_tokens
