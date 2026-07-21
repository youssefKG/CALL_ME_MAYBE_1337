from enum import Enum
from src.models.prompt_model import PromptModel
from src.models.function_definition_model import FunctionDefinitionModel
from typing_extensions import Self
from collections.abc import Generator

import json


class PromptGenerator:
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
    4. Otherwise, determine whether the value can be logically inferred from the request.
    5. If it cannot be inferred with confidence, output null.
    6. Never invent information.
    <think>
    - Output only the completed JSON object with no surrounding text.
    </think>

    Examples:
    Answer: {
    "prompt": "What is the sum of 2 and 3?",
    "name": "fn_add_numbers",
    "parameters": {"a": 2.0, "b": 3.0}
    }

    Answer: {
    "prompt": "Reverse the string 'hello'",
    "name": "fn_reverse_string",
    "parameters": {"s": "hello"}
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

    <think>

    <|im_start|>Answer:
    {"</think>
        "name": "{FUNCTION_NAME}",
        "prompt": "{USER_PROMPT}",
        "parameters": {
            {GENERATED_ARGUMENTS}"""

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
                PromptGenerator.PromptType.FUNCTIONS_NAME_STATIC.value.replace(
                    "{FUNCTIONS}", __get_fns_def()
                )
            )
            return self

        def set_function_argument_static_prompt(self) -> Self:
            self.__function_argument_static_prompt = (
                PromptGenerator.PromptType.FUNCTION_ARGUMENT_STATIC.value
            )
            return self

        def build(self) -> "PromptGenerator":
            return PromptGenerator(self)

        @property
        def functions_definitions(self) -> list[FunctionDefinitionModel]:
            return self.__functions_definitions

        @property
        def function_name_static_prompt(self) -> str:
            return self.__function_argument_static_prompt

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

    def iter_prompts(self) -> Generator[str]:
        for prompt in self.prompts:
            yield prompt.prompt

    def function_name_dynamic_prompt(self, prompt: str) -> str:
        return PromptGenerator.PromptType.FUNCTION_NAME_DYNAMIC.value.replace(
            "{USER_PROMPT}", prompt
        )

    def function_argument_dynamic_prompt(
        self,
        function_definition: FunctionDefinitionModel,
        user_prompt: str,
        generated_arguments: list[dict[str, bool | float | str]],
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

        def __format_generated_argument(
            generated_argument: list[dict[str, bool | float | str]],
            arg_name: str,
            arg_type: str,
        ) -> str:
            res: str = str()
            for arg in generated_argument:
                res += (
                    '    {"name": "{NAME}", "value": {VALUE}}, \n'.replace(
                        "{NAME}", arg["name"]
                    ),
                )
                if arg_type == "string":
                    res = res.replace("{VALUE}", f'"{arg.value}"')
                else:
                    res = res.replace("{VALUE}", arg.value)

            res += '    {"name": "{ARG_NAME}", "value": '.replace(
                "{ARG_NAME}", arg_name["name"]
            )
            if arg_type == "string":
                res += '"'
            return res

        return (
            PromptGenerator.PromptType.FUNCTION_ARGUMENET_DYNAMIC.value.replace(
                "{FUNCTION}", __format_the_function_prototype(function_definition)
            )
            .replace("{USER_PROMPT}", user_prompt)
            .replace("{FUNCTION_DESCRIPTION}", function_definition.description)
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
