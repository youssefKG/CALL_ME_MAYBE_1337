from enum import Enum

from src.Models.PromptJson import PromptModel, PromptsRootModel
from src.Models.FunctionDefinitionJson import FunctionDefinitionModel
from typing_extensions import Self
from collections.abc import Generator
import json


class PromptType(Enum):
    FUNCTIONS_DEFINITION_STATIC = """
    - Read the available function definitions.
    - Compare the user request against each function's description.
    - Select the function that best matches the user's intent.
    - Return ONLY the function name.
    - Do NOT return JSON.
    - Do NOT explain.
    - Do NOT output markdown.
    - Do NOT output any other text.

    Functions:

    {FUNCTIONS}

    Examples:

    Functions:
    - fn_add_numbers: Adds two numbers.
    - fn_greet: Greets a person by name.
    - fn_reverse_string: Reverses a string.

    User:
    What is the sum of 2 and 3?

    Output:
    fn_add_numbers

    Functions:
    - fn_add_numbers: Adds two numbers.
    - fn_greet: Greets a person by name.
    - fn_reverse_string: Reverses a string.

    User:
    Say hello to John.

    Output:
    fn_greet

    Functions:
    - fn_add_numbers: Adds two numbers.
    - fn_greet: Greets a person by name.
    - fn_reverse_string: Reverses a string.

    User:
    Reverse the word "hello".

    Output:
    fn_reverse_string"
    """

    FUNCTION_DEFINITION_DYNAMIC = """
    User request:

    {USER_PROMPT}
    """

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

        def set_static_fns_def_static_prompt(self) -> Self:
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
            print(prompt)
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


"""

public class User {
    private final String firstName; // required
    private final String lastName;  // required
    private final int age;          // optional
    private final String email;     // optional

    public static class Builder {
        private final String firstName;
        private final String lastName;
        private int age = 0;
        private String email = "";

        public Builder(String firstName, String lastName) {
            this.firstName = firstName;
            this.lastName = lastName;
        }

        public Builder age(int age) { this.age = age; return this; }
        public Builder email(String email) { this.email = email; return this; }

        public User build() {
            return new User(this);
        }
    }

    private User(Builder builder) {
        this.firstName = builder.firstName;
        this.lastName = builder.lastName;
        this.age = builder.age;
        this.email = builder.email;
    }
}

// Usage:
User user = new User.Builder("John", "Doe")
                .age(30)
                .email("john@example.com")
                .build();
"""
