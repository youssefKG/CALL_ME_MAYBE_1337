from pydantic import BaseModel


class FunctionParametresModel(BaseModel):
    type: str


class FunctionArgumentModel(BaseModel):
    type: str


class FunctionReturnModel(BaseModel):
    type: str


class FunctionDefnitionModel(BaseModel):
    name: str
    description: str
    parametres: list[FunctionParametresModel]
    returns: FunctionReturnModel
