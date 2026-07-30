"""Pydantic models for function definitions and their argument schemas."""

from typing import Literal, TypeAlias, Annotated
from pydantic import BaseModel, RootModel, StringConstraints
from pydantic import ConfigDict

ArgumentType: TypeAlias = Literal["string", "number", "boolean", "float", "integer"]


class TypeSpec(BaseModel):
    """Describes one supported argument type for a function definition.

    Specifies the type of a function parameter or return value, with
    validation to reject unknown type names.

    Attributes:
        type: One of the supported argument types.
    """
    type: ArgumentType
    model_config: ConfigDict = ConfigDict(extra="forbid")


class FunctionDefinitionModel(BaseModel):
    """Defines a callable function and its expected parameter schema.

    Represents the interface of one function available for function-call
    generation, including its name, description, and parameter types.

    Attributes:
        name: Function identifier (must be non-empty after stripping).
        description: Human-readable function description.
        parameters: Mapping of parameter names to their type specifications.
        returns: The type specification for the function's return value.
    """
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    description: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    parameters: dict[str, TypeSpec]
    returns: TypeSpec
    model_config: ConfigDict = ConfigDict(extra="forbid")


class FunctionsDefinitionRootModel(RootModel[list[FunctionDefinitionModel]]):
    """Root model for parsing a list of function definitions from JSON.

    Wraps a list of FunctionDefinitionModel objects for convenient JSON
    parsing and validation via Pydantic.
    """
    pass
