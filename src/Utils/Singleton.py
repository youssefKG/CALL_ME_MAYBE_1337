from typing_extensions import Self


class Singleton:
    __instance: Self | None = None

    def __new__(cls, *_args: complex, **_kwargs: complex) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
