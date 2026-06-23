from pydantic import BaseModel

class PromptJson(BaseModel):
    prompt: str

