from llm_sdk.llm_sdk import Small_LLM_Model
from src.utils.Singleton import Singleton
from Enums.ModelState import ModelState
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
            model_name,
            device=device,
            dtype=dtype,
            trust_remote_code=trust_remote_code,  # constructor
        )
        self.model_state: ModelState = ModelState.SelectingFunctionName

    def get_next_token(self, prompt: str) -> str:
        data_ids: list[int] = [int(x) for x in self.encode(prompt).flatten()]
        logits: list[float] = self.get_logits_from_input_ids(data_ids)
        prob_ids = torch.argmax(torch.tensor(logits), dim=-1).item()
        next_token: str = self.decode(torch.tensor(prob_ids))
        return next_token
