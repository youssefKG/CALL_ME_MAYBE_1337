import sys

from pydantic import ValidationError

from llm_model.model import Model
from src.parser.Parser import Parser

# from .llm_model.model import Model


def main() -> None:
    model = Model()


if __name__ == "__main__":
    main()
