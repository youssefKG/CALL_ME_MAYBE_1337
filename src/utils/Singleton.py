from typing_extensions import Self


class Singleton:
    __instance: Self | None = None

    def __new__(cls, file_name: str) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
