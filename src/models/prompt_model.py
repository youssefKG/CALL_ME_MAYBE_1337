"""Pydantic models for the prompt dataset consumed by the pipeline."""

from typing import Annotated
from uuid import uuid4

from pydantic import BaseModel, RootModel, Field, StringConstraints


class PromptModel(BaseModel):
    """Represents one user prompt in the input dataset.

    Encapsulates a user request that will be processed to generate a
    function call. Each prompt has a unique ID and the prompt text.

    Attributes:
        id: Unique identifier (auto-generated UUID if not provided).
        prompt: User's input text (must be non-empty after stripping).
    """

    id: str = Field(default_factory=lambda: str(uuid4()))
    prompt: Annotated[
        str, StringConstraints(min_length=1, strip_whitespace=True)
    ]  # prompt validation

    class Config:
        extra: str = "forbid"


class PromptsRootModel(RootModel[list[PromptModel]]):
    """Root model for parsing a list of prompts from JSON.

    Wraps a list of PromptModel objects for convenient JSON parsing and
    validation via Pydantic.
    """

    pass
