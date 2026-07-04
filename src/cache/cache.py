from src.utils.singleton import Singleton


class Cache(Singleton):
    def __init__(self) -> None:
        self.__fn_names_ids: list[int] = list()
        self.__fn_params_ids: list[int] = list()

    @property
    def get_fn_names_ids(self) -> list[int]:
        return self.__fn_params_ids

    @property
    def get_params_ids(self) -> list[int]:
        return self.__fn_params_ids

    def set_fns_def_static_prompt_ids(self, ids: list[int]) -> None:
        self.__fn_names_ids = ids

    def set_fn_params_static_prompt_ids(self, ids: list[int]) -> None:
        self.__fn_params_ids = ids
