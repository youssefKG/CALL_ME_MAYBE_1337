from typing import final

from typing_extensions import override


class A:
    def __init__(self) -> None:
        self._hello()

    def _hello(self) -> None:
        print("hello")


class B(A):

    @override
    def _hello(self) -> None:
        print("hello")
