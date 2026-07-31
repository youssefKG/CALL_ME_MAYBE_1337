"""Minimal singleton base class for shared runtime objects."""

from typing_extensions import Self


class Singleton:
    """Base class that ensures only one instance is created per process.

    Provides the singleton pattern to ensure a single shared instance
    of subclasses across the entire runtime. Subclasses inherit this
    behavior automatically.
    """

    __instance: Self | None = None

    def __new__(cls) -> Self:
        """Create or return the singleton instance.

        Implements lazy initialization, creating the instance on first
        access and returning the same instance on all subsequent calls.

        Returns:
            Self: The singleton instance of the class.
        """
        if cls.__instance is None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
