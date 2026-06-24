from llm_sdk.llm_sdk import Small_LLM_Model
from torch import Tensor


class Model(Small_LLM_Model):
    def __init__(self) -> None:
        super().__init__()

    def get_next_token(self, prompt: str) -> None:
        encoded_data: Tensor = self.encode(prompt)[0]
