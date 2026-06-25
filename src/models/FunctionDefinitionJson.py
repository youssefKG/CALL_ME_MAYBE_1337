from typing import Literal
from pydantic import BaseModel, RootModel


class TypeSpec(BaseModel):
    type: Literal["string", "number"]


class FunctionDefinition(BaseModel):
    name: str
    description: str
    parameters: dict[str, TypeSpec]
    returns: TypeSpec


class FunctionDefinitionModel(RootModel[list[FunctionDefinition]]): ...
