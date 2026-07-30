from pydantic import BaseModel, RootModel, StringConstraints
from typing import TypeAlias, Annotated

"""Pydantic models for generated function-call payloads."""

Argument: TypeAlias = dict[str, str | float | bool | int]


class FunctionCallModel(BaseModel):
    """Represents one generated function call with its resolved parameters."""
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    prompt: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    parameters: Argument


class FunctionCallRootModel(RootModel[list[FunctionCallModel]]): ...
