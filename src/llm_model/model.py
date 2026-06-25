from llm_sdk.llm_sdk import Small_LLM_Model
from src.utils.Singleton import Singleton
import torch


class Model(Small_LLM_Model, Singleton):

    def __init__(
        self,
        model_name: str = "Qwen/Qwen3-0.6B",
        *,
        device: str | None = None,
        dtype: torch.dtype | None = None,
        trust_remote_code: bool = True,
    ) -> None:
        super().__init__(
            model_name, device=device, dtype=dtype, trust_remote_code=trust_remote_code
        )

    def get_next_token(self, prompt: str) -> None:
        data_ids = self.encode(prompt).flatten().tolist()
        logits: list[float] = self.get_logits_from_input_ids(data_ids)
        print(logits)
