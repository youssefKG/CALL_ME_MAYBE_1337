from typing import final

from pydantic import BaseModel, RootModel, ConfigDict


class PromptModel(BaseModel):
    model_config: ConfigDict = ConfigDict(extra="forbid")
    prompt: str


class PromptsRootModel(RootModel[list[PromptModel]]): ...
