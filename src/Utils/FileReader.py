from .Singleton import Singleton


class File(Singleton):
    def __init__(self, file_name: str) -> None:
        self.file_name: str = file_name

    def read(self) -> str:
        return ""

    def write(self) -> None:
        pass

    def read_all(self) -> list[str]:
        return []
