import sys

from .parser.Parser import Parser


def main() -> None:
    try:
        parser: Parser = Parser(sys.argv)
        parser.parse()
    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()
