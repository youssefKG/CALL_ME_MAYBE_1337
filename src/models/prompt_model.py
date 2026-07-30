from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, RootModel, ConfigDict, Field, StringConstraints


class PromptModel(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    prompt: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    model_config: ConfigDict = ConfigDict(extra="forbid")


class PromptsRootModel(RootModel[list[PromptModel]]): ...
