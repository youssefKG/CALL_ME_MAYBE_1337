from pydantic import BaseModel


class PromptJsonModel(BaseModel):
    prompt: str
