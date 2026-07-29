from typing import final
from uuid import UUID, uuid4

from pydantic import BaseModel, RootModel, ConfigDict, Field


class PromptModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    model_config: ConfigDict = ConfigDict(extra="forbid")
    prompt: str


class PromptsRootModel(RootModel[list[PromptModel]]): ...
