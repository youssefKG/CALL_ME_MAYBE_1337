class FunctionParameter:
    def __init__(self, name: str, value: str) -> None:
        self.name: str = name
        self.value: str = value


class FunctionCall:
    def __init__(
        self,
    ) -> None:
        self.__name: str = str()
        self.__prompt: str = str()
        self.__arguments: list[FunctionParameter] = list()

    @property
    def name(self) -> str:
        return self.__name

    @property
    def prompt(self) -> str:
        return self.__prompt

    @property
    def arguments(self) -> list[FunctionParameter]:
        return self.__arguments

    @arguments.setter
    def arguments(self, arguments: list[FunctionParameter]) -> None:
        self.__arguments = arguments

    @prompt.setter
    def prompt(self, prompt: str) -> None:
        self.__prompt = prompt

    @name.setter
    def name(self, name: str) -> None:
        self.__name = name
