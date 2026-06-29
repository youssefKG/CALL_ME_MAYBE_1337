import sys
from src.Parser.Parser import Parser


def main() -> None:
    parser: Parser = Parser(sys.argv)
    parser.parse()


if __name__ == "__main__":
    main()
