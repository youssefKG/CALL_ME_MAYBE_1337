from pydantic import BaseModel, RootModel
from typing import TypeAlias

Argument: TypeAlias = dict[str, str | float | bool | int]


class FunctionCallModel(BaseModel):
    name: str
    prompt: str
    parameters: Argument


class FunctionCallRootModel(RootModel[list[FunctionCallModel]]): ...
