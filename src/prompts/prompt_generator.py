from enum import Enum

from src.utils.function import FunctionParameter
from src.models.prompt_model import PromptModel
from src.models.function_definition_model import FunctionDefinitionModel
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

    FUNCTION_PARAMETER_DYNAMIC = """
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

    def get_function_arguments_dynamic_prompt(
        self,
        function_definition: FunctionDefinitionModel,
        user_prompt: str,
        generated_arguments: list[FunctionParameter],
        arg_name: str,
        arg_type: str,
    ) -> str:

        return (
            PromptType.FUNCTION_PARAMETER_DYNAMIC.value.replace(
                "{FUNCTION}", self.__format_the_function_prototype(function_definition)
            )
            .replace("{USER_PROMPT}", user_prompt)
            .replace("{PARAMETER_NAME}", arg_name)
            .replace("{PARAMETER_TYPE}", arg_type)
            .replace(
                "{GENERATED_ARGUMENTS}",
                self.__format_generated_argument(
                    generated_arguments, arg_name, arg_type
                ),
            )
            .replace("{FUNCTION_DESCRIPTION}", function_definition.description)
            .replace("{FUNCTION_NAME}", function_definition.name)
        )

    def __format_generated_argument(
        self, generated_argument: list[FunctionParameter], arg_name: str, arg_type: str
    ) -> str:
        res: str = str()
        for idx, arg in enumerate(generated_argument):
            res += '    {"name": "{NAME}", "value": {VALUE}}, \n'.replace(
                "{NAME}", arg.name
            )
            if arg_type == "string":
                res = res.replace("{VALUE}", f'"{arg.value}"')
            else:
                res = res.replace("{VALUE}", arg.value)

        res += '    {"name": "{ARG_NAME}", "value": '.replace("{ARG_NAME}", arg_name)
        if arg_type == "string":
            res += '"'
        return res

    @property
    def get_fns_def_static_prompt(self) -> str:
        return self.__fns_def_static_prompt

    @property
    def get_function_argument_static_prompt(self) -> str:
        return self.__fn_params_static_prompt

    def __format_the_function_prototype(self, function: FunctionDefinitionModel) -> str:
        res: str = f"{function.name}("
        idx: int = 0
        function_params_len: int = len(function.parameters.items())
        for arg_name, arg_type in function.parameters.items():
            res += f"{arg_name}: {arg_type}"
            if idx < function_params_len - 1:
                res += ","
        res += ")"
        return res
