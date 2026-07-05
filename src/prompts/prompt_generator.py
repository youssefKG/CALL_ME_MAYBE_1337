from enum import Enum

from src.Models.PromptJson import PromptModel, PromptsRootModel
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
[
  {"name":"fn_add_numbers","description":"Add two numbers together and return their sum."},
  {"name":"fn_greet","description":"Generate a greeting message for a person by name."},
  {"name":"fn_reverse_string","description":"Reverse a string and return the reversed result."},
  {"name":"fn_get_square_root","description":"Calculate the square root of a number."},
  {"name":"fn_substitute_string_with_regex","description":"Replace all occurrences matching a regex pattern in a string."}
]
"""

    FUNCTION_DEFINITION_DYNAMIC = """
User request: {USER_PROMPT}

Answer: """

    FUNCTION_DEFINITION_PARAM_STATIC = """
    You are a function parameter extractor.

    Given:
    - a selected function definition
    - a user request

    Extract the arguments using these rules:

    - Use exact parameter names.
    - Use correct JSON types.
    - Infer values only when supported by the request.
    - Do not hallucinate missing values.
    - Required but unknown values must be null.
    - Omit optional unknown parameters.
    - Return only a valid JSON object.
    - No markdown.
    - No explanations.
    """

    FUNCTION_DEFINTION_PARAM_DYNAMIC = """
    Function:
    {FUNCTION}

    Request:
    {USER_PROMPT}
    """


class PromptGenerator:

    class Builder:
        def __init__(
            self,
            fns_def_json: FunctionDefinitionModel,
            prompts: PromptsRootModel,
        ) -> None:
            self.fns_def_json: FunctionDefinitionModel = fns_def_json
            self.prompts: PromptsRootModel = prompts
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
            self.fn_params_static_prompt = (
                PromptType.FUNCTION_DEFINITION_PARAM_STATIC.value
            )
            return self

        def build(self) -> "PromptGenerator":
            return PromptGenerator(self)

        @property
        def __get_fns_def(self) -> str:
            fn_names_desc: list[dict[str, str]] = list()

            for fn_def in self.fns_def_json:
                fn_names_desc.append(
                    {
                        "name": fn_def["name"],
                        "descritption": fn_def["description"],
                    }
                )
            return json.dumps(fn_names_desc)

    def __init__(self, builder: Builder) -> None:
        self.__functions_defintion_json: FunctionDefinitionModel = builder.fns_def_json
        self.prompts: PromptsRootModel = builder.prompts
        self.__fns_def_static_prompt: str = builder.fns_def_static_prompt
        self.__fn_params_static_prompt: str = builder.fn_params_static_prompt

    @property
    def next_prompt(self) -> Generator[str]:
        user_prompt: str
        for prompt in self.prompts:
            user_prompt = prompt["prompt"]
            yield user_prompt

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

