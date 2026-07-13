from typing import Literal
from pydantic import BaseModel, RootModel
from pydantic import ConfigDict


class TypeSpec(BaseModel):
    type: Literal["string", "number"]
    model_config: ConfigDict = ConfigDict(extra="forbid")


class FunctionDefinitionModel(BaseModel):
    name: str
    description: str
    parameters: dict[str, TypeSpec]
    returns: TypeSpec
    model_config: ConfigDict = ConfigDict(extra="forbid")


class FunctionsDefinitionRootModel(RootModel[list[FunctionDefinitionModel]]): ...
