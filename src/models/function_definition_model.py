from typing import Literal, TypeAlias
from pydantic import BaseModel, RootModel
from pydantic import ConfigDict

ArgumentType: TypeAlias = Literal["string", "number", "boolean", "float", "integer"]


class TypeSpec(BaseModel):
    type: ArgumentType
    model_config: ConfigDict = ConfigDict(extra="forbid")


class FunctionDefinitionModel(BaseModel):
    name: str
    description: str
    parameters: dict[str, TypeSpec]
    returns: TypeSpec
    model_config: ConfigDict = ConfigDict(extra="forbid")


class FunctionsDefinitionRootModel(RootModel[list[FunctionDefinitionModel]]): ...
