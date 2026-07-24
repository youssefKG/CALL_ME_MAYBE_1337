from pydantic import BaseModel, RootModel
from typing import TypeAlias

Argument: TypeAlias = dict[str, str | float | bool | int]


class FunctionCall(BaseModel):
    name: str
    prompt: str
    parameters: Argument


class FunctionsCall(RootModel[list[FunctionCall]]): ...
