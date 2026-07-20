from src.predictors.fn_param_predictor import FunctionParametersPredictor
from src.predictors.fn_name_predictor import FunctionNamePredictor
from src.LlmModel.model import Model
from src.prompts.prompt_generator import PromptGenerator
from src.utils.function import FunctionCall, FunctionParameter
from src.models.function_definition_model import FunctionDefinitionModel
from src.generator.function_name_generator import FunctionNameGenerator
from src.generator.function_parametre_generator import FunctionArgumentsGenerator


class OutputGenerator:
    def __init__(
        self,
        functions_definitions: list[FunctionDefinitionModel],
        model: Model,
        prompt_generator: PromptGenerator,
    ) -> None:
        self.__functions_definitions: list[FunctionDefinitionModel] = (
            functions_definitions
        )
        self.__model: Model = model
        self.__prompt_generator: PromptGenerator = prompt_generator
        self.__function_calls: list[FunctionCall] = list()
        self.__function_name_predictor: FunctionNamePredictor
        self.__function_parameters_predictor: FunctionParametersPredictor = (
            FunctionParametersPredictor()
        )
        self.__init_functions_name_predictor()

    def generate(self) -> None:
        for prompt in self.__prompt_generator.iter_prompts():
            function_definition: FunctionDefinitionModel | None = (
                self.__function_definition(prompt)
            )
            if function_definition:
                function_call: FunctionCall = FunctionCall(
                    function_definition.name,
                    prompt,
                    self.__function_arguments(function_definition, prompt),
                )
                self.__function_calls.append(function_call)

    def __function_definition(self, prompt: str) -> FunctionDefinitionModel | None:
        def __get_function_definition(
            function_name: str,
        ) -> FunctionDefinitionModel | None:
            for function_def in self.__functions_definitions:
                if function_def.name == function_name:
                    return function_def
            return None

        function_name_generator: FunctionNameGenerator = FunctionNameGenerator(
            model=self.__model,
            function_name_predictor=self.__function_name_predictor,
            prompt_generator=self.__prompt_generator,
            prompt=prompt,
        )
        function_name_generator.generate()
        return __get_function_definition(function_name_generator.fn_name)

    def __function_arguments(
        self, function_definition: FunctionDefinitionModel, prompt: str
    ) -> list[FunctionParameter]:
        function_argument_generator = FunctionArgumentsGenerator(
            prompt_generator=self.__prompt_generator,
            user_prompt=prompt,
            function_definition=function_definition,
            model=self.__model,
            function_parameters_predictor=self.__function_parameters_predictor,
        )
        function_argument_generator.generate()
        return function_argument_generator.function_arguments

    def __init_functions_name_predictor(self) -> None:
        self.__function_name_predictor = FunctionNamePredictor()
        fns_def_names_ids: list[list[int]] = list()
        for fn_def in self.__functions_definitions:
            fns_def_names_ids.append(self.__model.encode_text(fn_def.name))
        self.__function_name_predictor.set_fns_names_ids_trie(fns_def_names_ids)
