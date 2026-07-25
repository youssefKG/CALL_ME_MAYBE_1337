from log.log import Log, LogRow
from src.predictors.fn_param_predictor import FunctionParametersPredictor
from src.predictors.fn_name_predictor import FunctionNamePredictor
from src.llm.model import Model
from src.prompts.prompt_generator import PromptGenerator
from src.models.functions_call import FunctionCall, Argument, FunctionsCall
from src.models.function_definition_model import FunctionDefinitionModel
from src.generator.function_name_generator import FunctionNameGenerator
from src.generator.function_parametre_generator import FunctionArgumentsGenerator
from src.log.log import Log


class OutputGenerator:
    def __init__(
        self,
        functions_definitions: list[FunctionDefinitionModel],
        model: Model,
        prompt_generator: PromptGenerator,
        output_path: str,
    ) -> None:
        self.__functions_definitions: list[FunctionDefinitionModel] = (
            functions_definitions
        )
        self.__model: Model = model
        self.__log: Log = Log()
        self.__prompt_generator: PromptGenerator = prompt_generator
        self.__functions_calls: list[FunctionCall] = list()
        self.__function_name_predictor: FunctionNamePredictor
        self.__function_parameters_predictor: FunctionParametersPredictor = (
            FunctionParametersPredictor()
        )
        self.__output_path: str = output_path
        self.__init_functions_name_predictor()
        self.__init_log()

    def generate(self) -> None:
        for id, prompt in enumerate(self.__prompt_generator.iter_prompts()):
            function_definition: FunctionDefinitionModel | None = (
                self.__function_definition(prompt)
            )
            if function_definition:
                self.__log.add_row(
                    LogRow(id, prompt, function_definition.model_dump_json(indent=4))
                )
                function_call: FunctionCall = FunctionCall(
                    name=function_definition.name,
                    prompt=prompt,
                    parameters=self.__function_arguments(function_definition, prompt),
                )
                self.__functions_calls.append(function_call)
                print(function_call.model_dump_json(indent=4))
        self.__generate_output_file()

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
    ) -> Argument:
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

    @property
    def functions_calls(self) -> list[FunctionCall]:
        return self.__functions_calls

    def __generate_output_file(self) -> None:
        try:
            with open(self.__output_path, "w") as output_file:
                functions_calls_json: str = FunctionsCall(
                    self.__functions_calls
                ).model_dump_json(indent=4)
                output_file.write(functions_calls_json)
        except Exception:
            pass

    def __init_log(self) -> None:
        self.__log.add_rows(
            [
                LogRow(id, prompt)
                for id, prompt in enumerate(self.__prompt_generator.iter_prompts())
            ]
        )
