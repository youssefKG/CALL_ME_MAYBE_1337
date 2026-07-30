from typing import Literal, TypeAlias, Annotated
from pydantic import BaseModel, RootModel, StringConstraints
from pydantic import ConfigDict

ArgumentType: TypeAlias = Literal["string", "number", "boolean", "float", "integer"]


class TypeSpec(BaseModel):
    type: ArgumentType
    model_config: ConfigDict = ConfigDict(extra="forbid")


class FunctionDefinitionModel(BaseModel):
    name: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    description: Annotated[str, StringConstraints(min_length=1, strip_whitespace=True)]
    parameters: dict[str, TypeSpec]
    returns: TypeSpec
    model_config: ConfigDict = ConfigDict(extra="forbid")


class FunctionsDefinitionRootModel(RootModel[list[FunctionDefinitionModel]]): ...
