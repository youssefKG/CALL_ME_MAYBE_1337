import sys
from pydantic import ValidationError
from src.llm_model.model import Model
from src.parser.Parser import Parser


def main() -> None:
    model = Model()
    print(model.get_next_token("hello world"))


if __name__ == "__main__":
    main()
