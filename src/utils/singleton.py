"""Minimal singleton base class for shared runtime objects."""

from typing_extensions import Self


class Singleton:
    """Base class that ensures only one instance is created per process."""
    __instance: Self | None = None

    def __new__(cls) -> Self:
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
