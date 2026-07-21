class FunctionParameter:
    def __init__(self, name: str, value: str | float) -> None:
        self.name: str = name
        self.value: str | float = value


class FunctionCall:
    def __init__(
        self, name: str, prompt: str, arguments: list[FunctionParameter]
    ) -> None:
        self.__name: str = name
        self.__prompt: str = prompt
        self.__arguments: list[FunctionParameter] = arguments

    @property
    def name(self) -> str:
        return self.__name

    @property
    def prompt(self) -> str:
        return self.__prompt

    @property
    def arguments(self) -> list[FunctionParameter]:
        return self.__arguments
