from Enums.ModelState import ModelState
from Enums.PromptType import PromptType
from src.Models.FunctionDefinitionJson import FunctionDefinitionModel
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
        prompt: str =  self.__get_prompt(model_state)

    def __build_prompt_for_function_name(
        self, prompt: str, functions_raw_json: str
    ) -> str:
        return PromptType.FUNCTION_NAME.value.replace(
            "{FUNCTIONS}", functions_raw_json
        ).replace(  # replace
            "{USER_PROMPT}", prompt
        )

    def __get_functions_name_raw_json(self) -> str:
        functions_names: list[dict[str, str]] = list()

        for function in self.__functions_defintion_json:
            functions_names.append(
                {"name": function.name, "descritption": function.descritption}
            )
        return json.dumps(functions_names)

    def __get_prompt(self, model_state: ModelState) -> str:
        match model_state:
            case ModelState.SelectingFunctionName:
                return self.SelectingFunctionName.value
            case _:
                return ""
    def set_functions_definition_in_prompt(self, excluded_funcs: list[str]) ->  str
        pass


class PromptBuilder:
    pass
