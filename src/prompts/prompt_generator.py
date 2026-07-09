from enum import Enum

from src.Models.PromptJson import PromptModel
from src.Models.FunctionDefinitionJson import FunctionDefinitionModel
from typing_extensions import Self
from collections.abc import Generator
import json


class PromptType(Enum):
    FUNCTIONS_DEFINITION_STATIC = """
    Instructions:
    - Read the available function definitions.
    - Select the single function that best matches the user's request.
    - Return ONLY the function name.
    - Do not explain.
    - Do not repeat the user request.
    - If the best function is fn_add_numbers, output exactly: fn_add_numbers
    - Do NOT output anything else.

    Functions:
    {FUNCTIONS}
    """

    FUNCTION_DEFINITION_DYNAMIC = """
    User request: {USER_PROMPT}
    Answer: """

    FUNCTION_PARAMETER_STATIC = """
    You are extracting one function argument at a time.

    You are given:
    - The function definition.
    - The user request.
    - The arguments that have already been extracted.

    Your task is to extract ONLY the requested parameter.

    Rules:
    - Return only the value.
    - Use the required type.
    - Use the already extracted arguments as context.
    - Do not change previously extracted arguments.
    - Do not invent values.
    - If the value cannot be determined, return null.
    - No JSON.
    - No markdown.
    - No explanations.
    """

    FUNCTION_PARAMETER_DYNAMIC = """
    Function:
    {FUNCTION}

    User request:
    {USER_PROMPT}

    Parameter to extract:
    - Name: {PARAMETER_NAME}
    - Type: {PARAMETER_TYPE}

    Generated arguments:
    {GENERATED_ARGUMENTS}

    Extract the value for the parameter "{PARAMETER_NAME}".

    Answer:
    """


class PromptGenerator:

    class Builder:
        def __init__(
            self,
            fns_def_json: list[FunctionDefinitionModel],
            prompts: list[PromptModel],
        ) -> None:
            self.fns_def: list[FunctionDefinitionModel] = fns_def_json
            self.prompts: list[PromptModel] = prompts
            self.fns_def_static_prompt: str
            self.fn_params_static_prompt: str

        def set_fns_def_static_prompt(self) -> Self:
            self.fns_def_static_prompt = (
                PromptType.FUNCTIONS_DEFINITION_STATIC.value.replace(
                    "{FUNCTIONS}", self.__get_fns_def
                )
            )
            return self

        def set_params_static_prompt(self) -> Self:
            self.fn_params_static_prompt = PromptType.FUNCTION_PARAMETER_STATIC.value
            return self

        def build(self) -> "PromptGenerator":
            return PromptGenerator(self)

        @property
        def __get_fns_def(self) -> str:
            fn_names_desc: list[dict[str, str]] = list()

            for fn_def in self.fns_def:
                fn_names_desc.append(
                    {"name": fn_def.name, "descritption": fn_def.description}
                )
            return json.dumps(fn_names_desc)

    def __init__(self, builder: Builder) -> None:
        self.__functions_defintion: list[FunctionDefinitionModel] = builder.fns_def
        self.prompts: list[PromptModel] = builder.prompts
        self.__fns_def_static_prompt: str = builder.fns_def_static_prompt
        self.__fn_params_static_prompt: str = builder.fn_params_static_prompt

    @property
    def next_prompt(self) -> Generator[str | None]:
        for prompt in self.prompts:
            yield prompt.prompt
        yield None

    def get_fns_def_dynamic_prompt(self, prompt: str) -> str:
        return PromptType.FUNCTION_DEFINITION_DYNAMIC.value.replace(
            "{USER_PROMPT}", prompt
        )

    @property
    def get_fns_def_static_prompt(self) -> str:
        return self.__fns_def_static_prompt

    @property
    def get_fn_params_static_prompt(self) -> str:
        return self.__fn_params_static_prompt

    def get_fn_def_by_name(self, name: str) -> FunctionDefinitionModel | None:
        for fn_def in self.__functions_defintion:
            if fn_def.name == name:
                return fn_def
        return None
