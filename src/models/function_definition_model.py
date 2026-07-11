from typing import Literal
from pydantic import BaseModel, RootModel


class TypeSpec(BaseModel):
    type: Literal["string", "number"]


class FunctionDefinitionModel(BaseModel):
    name: str
    description: str
    parameters: dict[str, TypeSpec]
    returns: TypeSpec


class FunctionsDefinitionRootModel(RootModel[list[FunctionDefinitionModel]]):
    pass
