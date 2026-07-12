class FunctionParameter:
    def __init__(self, name: str, value: str) -> None:
        self.name: str = name
        self.value: str = value


class FunctionCall:
    def __init__(
        self,
        name: str,
        prompt: str = "null",
        parameters: list[FunctionParameter] | None = None,
    ) -> None:
        self.name: str = name
        self.prompt: str = prompt
        self.parameters: list[FunctionParameter] | None = parameters
