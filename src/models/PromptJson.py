from pydantic import BaseModel, RootModel


class PromptModel(BaseModel):
    prompt: str


class PromptsRootModel(RootModel[list[PromptModel]]): ...
