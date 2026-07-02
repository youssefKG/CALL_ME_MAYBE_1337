from typing import final

from pydantic import BaseModel, RootModel, ConfigDict
from typing_extensions import override


class PromptModel(BaseModel):
    prompt: str
    model_config = ConfigDict(extra="forbid")


class PromptsRootModel(RootModel[list[PromptModel]]): ...
