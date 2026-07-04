from src.LlmModel.model import Model
from src.Parser.Parser import Parser
from src.prompts.prompt_generator import PromptGenerator
import numpy as np
from src.cache.cache import Cache
import torch


class Generator:
    def __init__(self, parser: Parser) -> None:
        self.__model: Model = Model()
        self.__cache = Cache()
        self.__parser: Parser = parser
        self.__prompt_generator: PromptGenerator = (
            PromptGenerator.Builder(
                self.__parser.get_fns_def,
                self.__parser.get_prompts
            )
            .set_params_static_prompt()
            .set_fns_def_static_prompt()
            .build()
        )

    def init_cache(self) -> None:
        encoded_fns_def_names_ids: list[int] = self.__model.encode(
            self.__prompt_generator.get_fn_params_static_prompt
        )
        print(self.__prompt_generator.get_fns_def_static_prompt)
        encoded_fn_def_params_ids: list[int] = self.__model.encode(
            self.__prompt_generator.get_fns_def_static_prompt
        )
        self.__cache.set_fns_def_static_prompt_ids(encoded_fns_def_names_ids)
        self.__cache.set_fn_params_static_prompt_ids(encoded_fn_def_params_ids)

    @property
    def get_fns_def_static_prompt(self) -> None:
        return self.__cache.get_params_ids
    
    def generate_prompt_ids(self, text: str | None = None) -> list[int]:
        text_ids: list[int] = []
        if text is None:
            text_ids = []
        def generate() -> list[int]:
            nonlocal text_ids
            prompt: str = next(self.__prompt_generator.next_prompt)
            fns_def_dynamic_prompt: str = (
                    self.__prompt_generator.get_fns_def_dynamic_prompt(prompt)
            )
            fns_def_dynamic_prompt_ids: list[int] = self.__model.encode(fns_def_dynamic_prompt)
            fns_static_prompts_ids: list[int] = self.__cache.get_params_ids
            text_ids +=  fns_def_dynamic_prompt_ids + fns_static_prompts_ids
            return text_ids


    def get_next_token(self, text_ids: list[int]) -> int:
        res: int
        logits: list[float] = self.__model.get_logits(text_ids)
        props_ids = torch.argmax(torch.tensor(logits), dim=-1).item()
        token: str = self.__model.decode(props_ids)
        return token
