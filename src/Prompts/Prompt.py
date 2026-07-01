from enum import Enum

from Models.PromptJson import PromptModel, PromptsRootModel
from predictors import fn_name_predictor
from src.Enums.ModelState import ModelState
from src.Enums.PromptType import PromptType
from src.Models.FunctionDefinitionJson import FunctionDefinitionModel
from typing_extensions import Self
from typing import cast
from collections.abc import Generator
import json


class PromptMode(Enum):
    FN_NAME = """
    You are a function selector.

    Functions:
    {FUNCTIONS}

    Task:

    Read the user request.
    Choose the function whose description best matches the request.
    Return ONLY the function name.
    Do not explain.
    Do not output JSON.
    Do not output any other text.

    Examples:

    User: What is the sum of 2 and 3?
    Output: fn_add_numbers

    User: Greet John
    Output: fn_greet

    User: Reverse hello
    Output: fn_reverse_string

    User:
    {USER_PROMPT}

    Output: {"
    """

    FN_PARAMS = """
    You are a parameter extractor.

    The function has already been selected.

    Function:

    {FUNCTION}

    User request:

    {USER_PROMPT}

    Task:

    * Extract the arguments for this function.
    * Use the exact parameter names.
    * Use the correct parameter types.
    * Return ONLY a JSON object containing the parameters.
    * Do not include the function name.
    * Do not explain.
    * Do not output any other text.

    Examples:

    Function:
    fn_add_numbers(a: number, b: number)

    User:
    What is the sum of 2 and 3?

    Output:
    {"a":2,"b":3}

    Function:
    fn_greet(name: string)

    User:
    Greet John

    Output:
    {"name":"John"}

    Function:
    {FUNCTION}

    User:
    {USER_PROMPT}

    Output: {"
    """


class PromptManager:
    def __init__(
        self,
        functions_definition_json: FunctionDefinitionModel,
        prompts: PromptsRootModel,
    ) -> None:
        self.__functions_defintion_json: FunctionDefinitionModel = (
            functions_definition_json
        )
        self.prompts: PromptsRootModel = prompts
        self.prompt_mode: PromptMode = PromptMode.FN_NAME
        self.current_prompt: str

    def generate(self) -> str:
        # return self.__functions_defintion_json
        match self.prompt_mode:
            case PromptMode.FN_NAME:
                return (
                    self.__get_prompt()
                    .__set_user_prompt()
                    .__set_argument_or_functions()
                    .__end()
                )
            case PromptMode.FN_PARAMS:
                pass
        return ""

    def __end(self) -> str:
        if self.prompt_mode == PromptMode.FN_NAME:
            self.prompt_mode = PromptMode.FN_PARAMS
        elif self.prompt_mode == PromptMode.FN_PARAMS:
            self.prompt_mode = PromptMode.FN_NAME
        return self.current_prompt

    def __get_functions_name_raw_json(self) -> str:
        fn_names_desc: list[dict[str, str]] = list()

        for fn_def in self.__functions_defintion_json:
            fn_names_desc.append(
                {
                    "name": fn_def["name"],
                    "descritption": fn_def["description"],
                }
            )
        return json.dumps(functions_names)

    def __get_prompt(self) -> Self:
        match self.prompt_mode:
            case ModelState.SelectingFunctionName:
                self.current_prompt = PromptType.FUNCTION_NAME.value
            case _:
                pass
        return self

    def __set_user_prompt(self) -> Self:
        user_prompt: str = next(self.__get_user_prompt())
        self.current_prompt = self.current_prompt.replace("{USER_PROMPT}", user_prompt)
        return self

    def __set_argument_or_functions(self) -> Self:
        match self.prompt_mode:
            case ModelState.SelectingFunctionName:
                functions: str = self.__get_functions_name_raw_json()
                self.current_prompt = self.current_prompt.replace(
                    "{FUNCTIONS}", functions
                )
            case _:
                pass
        return self

    def __get_user_prompt(self) -> Generator[str]:
        user_prompt: str
        for prompt in self.prompts:
            user_prompt = cast(PromptModel, cast(object, prompt)).prompt
            yield user_prompt


def test_prompt_manager(
    functions_definition_json: FunctionDefinitionModel, prompts: PromptModel
) -> None:

    prompt_manager: PromptManager = PromptManager(functions_definition_json, prompts)
