from enum import Enum

from src.models import PromptModel, FunctionDefinitionModel
from typing_extensions import Self
from collections.abc import Generator

import json


class PromptType(str, Enum):
    FUNCTIONS_NAME_STATIC = """
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

    FUNCTION_NAME_DYNAMIC = """
    User request: {USER_PROMPT}
    Answer: """

    FUNCTION_ARGUMENT_STATIC = """
    <|im_start|>
    You are completing a function call.

    The selected function has already been determined.

    Your task is to complete the "parameters" field using:
    - the function definition,
    - the function description,
    - and the user request.

    For each parameter:
    1. Read the parameter name and description.
    2. Search the user's request for an explicit value.
    3. If an explicit value exists, copy it exactly.
    4. Never invent information.
    5- Take if from examples if it possible

    Examples:
    Answer: {
    "prompt": "Replace all vowels in 'Programming is fun' with asterisks"
    "name": "fn_substitute_string_with_regex",
    "parameters": {
        'source_string': 'Programming is fun',
        'regex': '[aeiouAEIOU]',
        'replacement': '*'
        }
    }

    Answer: {
    "prompt": "Replace all numbers in \"Hello 34 I'm 233 years old\" with NUMBERS"
    "name": "fn_substitute_string_with_regex",
    "parameters": {
        'source_string': "Hello 34 I'm 233 years old",
        'regex': '\\d+',
        'replacement': 'NUMBERS'
        }
    }
    """

    FUNCTION_ARGUMENET_DYNAMIC = """
    Function:
    {FUNCTION}

    Description:
    {FUNCTION_DESCRIPTION}

    User request:
    {USER_PROMPT}
    <|im_end|>

    Answer:
    """

    FUNCTION_CALL = """{
        "name": "{FUNCTION_NAME}",
        "prompt": "{USER_PROMPT}",
        "parameters": {
            {GENERATED_ARGUMENTS}"""


class PromptGenerator:
    class Builder:
        def __init__(
            self,
        ) -> None:
            self.__functions_definitions: list[FunctionDefinitionModel]
            self.__prompts: list[PromptModel]
            self.__function_name_static_prompt: str
            self.__function_argument_static_prompt: str

        def set_function_definitions(
            self, functions_definitions: list[FunctionDefinitionModel]
        ) -> Self:
            self.__functions_definitions = functions_definitions
            return self

        def set_prompts(self, prompt: list[PromptModel]) -> Self:
            self.__prompts = prompt
            return self

        def set_function_name_static_prompt(self) -> Self:
            def __get_fns_def() -> str:
                function_info: list[dict[str, str]] = list()
                for fn_def in self.__functions_definitions:
                    function_info.append(
                        {"name": fn_def.name, "descritption": fn_def.description}
                    )
                return json.dumps(function_info)

            self.__function_name_static_prompt = (
                PromptType.FUNCTIONS_NAME_STATIC.value.replace(
                    "{FUNCTIONS}", __get_fns_def()
                )
            )
            return self

        def set_function_argument_static_prompt(self) -> Self:
            self.__function_argument_static_prompt = (
                PromptType.FUNCTION_ARGUMENT_STATIC.value
            )
            return self

        def build(self) -> "PromptGenerator":
            return PromptGenerator(self)

        @property
        def functions_definitions(self) -> list[FunctionDefinitionModel]:
            return self.__functions_definitions

        @property
        def function_name_static_prompt(self) -> str:
            return self.__function_name_static_prompt

        @property
        def function_argument_static_prompt(self) -> str:
            return self.__function_argument_static_prompt

        @property
        def prompts(self) -> list[PromptModel]:
            return self.__prompts

    def __init__(self, builder: Builder) -> None:
        self.__functions_defintion: list[FunctionDefinitionModel] = (
            builder.functions_definitions
        )
        self.prompts: list[PromptModel] = builder.prompts
        self.__function_name_static_prompt: str = builder.function_name_static_prompt
        self.__function_arguments_static_prompt: str = (
            builder.function_argument_static_prompt
        )

    def iter_prompts(self) -> Generator[PromptModel]:
        for prompt in self.prompts:
            yield prompt

    def function_name_dynamic_prompt(self, prompt: str) -> str:
        return PromptType.FUNCTION_NAME_DYNAMIC.value.replace("{USER_PROMPT}", prompt)

    def function_argument_dynamic_prompt(
        self,
        function_definition: FunctionDefinitionModel,
        user_prompt: str,
        generated_arguments: dict[str, bool | float | str | int],
        arg_name: str,
        arg_type: str,
    ) -> str:

        def __format_the_function_prototype(function: FunctionDefinitionModel) -> str:
            res: str = f"{function.name}("
            idx: int = 0
            function_params_len: int = len(function.parameters.items())
            for arg_name, arg_type in function.parameters.items():
                res += f"{arg_name}: {arg_type}"
                if idx < function_params_len - 1:
                    res += ","
            res += ")"
            return res

        function_argument_description: str = (
            PromptType.FUNCTION_ARGUMENET_DYNAMIC.value.replace(
                "{FUNCTION}", __format_the_function_prototype(function_definition)
            )
            .replace("{FUNCTION_DESCRIPTION}", function_definition.description)
            .replace("{USER_PROMPT}", user_prompt)
        )
        function_call: str = self.function_call_prompt(
            user_prompt, function_definition, generated_arguments, arg_name, arg_type
        )

        return function_argument_description + function_call

    def function_call_prompt(
        self,
        user_prompt: str,
        function_definition: FunctionDefinitionModel,
        generated_arguments: dict[str, str | float | bool],
        arg_name: str,
        arg_type: str,
    ) -> str:
        def __format_generated_argument(
            generated_argument: dict[str, str | float | bool],
            arg_name: str,
            arg_type: str,
        ) -> str:
            res: str = str()
            for name, value in generated_argument.items():
                res += '"{NAME}": "{VALUE}", '.replace("{NAME}", name).replace(
                    "{VALUE}" if isinstance(value, str) else '"{VALUE}"', str(value)
                )

            res += '"{NAME}": {VALUE}'.replace("{NAME}", arg_name).replace(
                "{VALUE}", '"' if arg_type == "string" else ""
            )
            return res

        return (
            PromptType.FUNCTION_CALL.value.replace("{USER_PROMPT}", user_prompt)
            .replace("{FUNCTION_NAME}", function_definition.name)
            .replace(
                "{GENERATED_ARGUMENTS}",
                __format_generated_argument(generated_arguments, arg_name, arg_type),
            )
        )

    @property
    def function_name_static_prompt(self) -> str:
        return self.__function_name_static_prompt

    @property
    def function_argument_static_prompt(self) -> str:
        return self.__function_arguments_static_prompt
