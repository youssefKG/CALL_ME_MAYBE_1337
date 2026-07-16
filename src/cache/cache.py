from src.utils.singleton import Singleton


class Cache(Singleton):
    def __init__(self) -> None:
        self.__fn_names_ids: list[int] = list()
        self.__function_argument_static_prompt_ids: list[int]
        self.__im_end_id: int
        self.__numbers_ids: list[int] = list()
        self.__ascii_ids: list[int] = list()
        self.__null_ids: list[int] = list()

    @property
    def get_function_name_static_prompt_ids(self) -> list[int]:
        return self.__fn_names_ids

    def set_fns_def_static_prompt_ids(self, ids: list[int]) -> None:
        self.__fn_names_ids = ids

    @property
    def get_function_argument_static_prompt_ids(self) -> list[int]:
        return self.__function_argument_static_prompt_ids

    def set_function_argument_static_prompt_ids(self, ids: list[int]) -> None:
        self.__function_argument_static_prompt_ids = ids

    def set_im_end_id(self, id: int) -> None:
        self.__im_end_id = id

    @property
    def im_end_id(self) -> int:
        return self.__im_end_id

    def set_numbers_ids(self, ids: list[int]) -> None:
        self.__numbers_ids += ids

    @property
    def get_numbers_ids(self) -> list[int]:
        return self.__numbers_ids

    def set_ascii_ids(self, ids: list[int]) -> None:
        self.__ascii_ids = ids

    @property
    def get_ascii_ids(self) -> list[int]:
        return self.__ascii_ids

    def set_null_id(self, ids: list[int]) -> None:
        self.__null_ids = ids

    @property
    def get_null_ids(self) -> list[int]:
        return self.__null_ids
