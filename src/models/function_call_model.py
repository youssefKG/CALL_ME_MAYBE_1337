from pydantic import BaseModel, RootModel, StringConstraints
from typing import TypeAlias, Annotated

Argument: TypeAlias = dict[str, str | float | bool | int]


class FunctionCallModel(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    prompt: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    parameters: Argument


class FunctionCallRootModel(RootModel[list[FunctionCallModel]]): ...
