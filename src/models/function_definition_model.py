from typing import Literal, TypeAlias, Annotated
from pydantic import BaseModel, RootModel, StringConstraints
from pydantic import ConfigDict

"""Pydantic models for function definitions and their argument schemas."""

ArgumentType: TypeAlias = Literal["string", "number", "boolean", "float", "integer"]


class TypeSpec(BaseModel):
    """Describes one supported argument type for a function definition."""
    type: ArgumentType
    model_config: ConfigDict = ConfigDict(extra="forbid")


class FunctionDefinitionModel(BaseModel):
    """Defines a callable function and its expected parameter schema."""
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    description: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    parameters: dict[str, TypeSpec]
    returns: TypeSpec
    model_config: ConfigDict = ConfigDict(extra="forbid")


class FunctionsDefinitionRootModel(RootModel[list[FunctionDefinitionModel]]): ...
