from src.Enums.ModelState import ModelState
from src.Enums.PromptType import PromptType
from src.Models.FunctionDefinitionJson import FunctionDefinitionModel
from typing_extensions import Self
import json


class Prompt:
    def __init__(
        self,
        functions_definition_json: FunctionDefinitionModel,
    ) -> None:
        self.__prompt_template: str = """ Output: """
        self.__functions_defintion_json: FunctionDefinitionModel = (
            functions_definition_json
        )
        self.prompt: str

    def generate(self, user_prompt: str, model_state: ModelState) -> str:
        # return self.__functions_defintion_json
        return (
            self.__get_prompt(model_state)
            .__set_user_prompt(user_prompt)
            .__set_argument_or_functions(model_state)
            .__end()
        )

    def __end(self) -> str:
        return self.prompt

    def __get_functions_name_raw_json(self) -> str:
        functions_names: list[dict[str, str]] = list()

        for function in self.__functions_defintion_json:
            functions_names.append(
                {
                    "name": function["name"],
                    "descritption": function["description"],
                }
            )
        return json.dumps(functions_names)

    def __get_prompt(self, model_state: ModelState) -> Self:
        match model_state:
            case ModelState.SelectingFunctionName:
                self.prompt = PromptType.FUNCTION_NAME.value
            case _:
                pass
        return self

    def __set_user_prompt(self, user_prompt: str) -> Self:
        self.prompt = self.prompt.replace("{USER_PROMPT}", user_prompt)
        return self

    def __set_argument_or_functions(self, model_state: ModelState) -> Self:
        match model_state:
            case ModelState.SelectingFunctionName:
                functions: str = self.__get_functions_name_raw_json()
                self.prompt = self.prompt.replace("{FUNCTIONS}", functions)
            case _:
                pass
        return self


class PromptBuilder:
    pass
