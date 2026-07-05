from src.LlmModel.model import Model
from src.Parser.Parser import Parser
from src.prompts.prompt_generator import PromptGenerator
from src.cache.cache import Cache
import torch


class Generator:
    def __init__(self, parser: Parser) -> None:
        self.__model: Model = Model()
        self.__cache = Cache()
        self.__parser: Parser = parser
        self.__prompt_generator: PromptGenerator = (
            PromptGenerator.Builder(
                self.__parser.get_fns_def, self.__parser.get_prompts
            )
            .set_params_static_prompt()
            .set_fns_def_static_prompt()
            .build()
        )
        self.__init_cache()

    def generate_prompt_ids(self, prompt: str) -> callable:
        text_ids: list[int] = list()
        fns_def_dynamic_prompt: str = (
            self.__prompt_generator.get_fns_def_dynamic_prompt(prompt)
        )
        fns_def_dynamic_prompt_ids: list[int] = self.__model.encode_text(
            fns_def_dynamic_prompt
        )
        fns_static_prompts_ids: list[int] = self.__cache.get_params_ids
        text_ids += fns_def_dynamic_prompt_ids + fns_static_prompts_ids
        print(self.__prompt_generator.get_fns_def_static_prompt, end="")
        print(fns_def_dynamic_prompt, end="")

        def generate(token_id: int | None = None) -> list[int]:
            nonlocal text_ids
            if token_id is None:
                return text_ids
            text_ids.append(token_id)
            return text_ids

        return generate

    def get_next_token(self, text_ids: list[int]) -> tuple[str, int]:
        logits: list[float] = self.__model.get_logits(text_ids)
        props_ids = torch.argmax(torch.tensor(logits), dim=-1).item()
        token: str = self.__model.decode(torch.tensor(props_ids))
        token_id: int = self.__model.encode_text(token)[0]
        return (token, token_id)

    @property
    def next_prompt(self) -> str:
        return next(self.__prompt_generator.next_prompt)

    def __init_cache(self) -> None:
        encoded_fns_def_names_ids: list[int] = self.__model.encode_text(
            self.__prompt_generator.get_fn_params_static_prompt
        )
        encoded_fn_def_params_ids: list[int] = self.__model.encode_text(
            self.__prompt_generator.get_fns_def_static_prompt
        )
        self.__cache.set_fns_def_static_prompt_ids(encoded_fns_def_names_ids)
        self.__cache.set_fn_params_static_prompt_ids(encoded_fn_def_params_ids)


"""

You are a function selector.

Instructions:
- Read the available function definitions.
- Select the single function that best matches the user's request.
- Return ONLY the function name.
- Do NOT explain.
- Do NOT output anything else.

Functions:
[{"name": "fn_add_numbers", "descritption": "Add two numbers together and return their sum."}, {"name": "fn_greet", "descritption": "Generate a greeting message for a person by name."}, {"name": "fn_reverse_string", "descritption": "Reverse a string and return the reversed result."}, {"name": "fn_get_square_root", "descritption": "Calculate the square root of a number."}, {"name": "fn_substitute_string_with_regex", "descritption": "Replace all occurrences matching a regex pattern in a string."}]

Examples:

User: What is the sum of 0 and 3?
Answer: fn_add_numbers

User: Say hello to John.
Answer: fn_greet

User: Reverse the word "hello".
Answer: fn_reverse_string

User: What is the square root of 48?
Answer: fn_get_square_root

Now answer this.

User: What is the sum of 1 and 3?
Answer:
 What is the sum of 1 and 3%

"""
