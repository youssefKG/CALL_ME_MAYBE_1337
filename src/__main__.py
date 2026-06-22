import sys
from .parser.ArgParser import ArgsParser


def main() -> None:
    try:
        args_parser = ArgsParser(sys.argv)
        args_parser.parse()
    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()
