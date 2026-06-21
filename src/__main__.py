import sys
from .parser.ArgParser import ArgsParser


def main() -> None:
    try:
        ArgsParser.check_args(sys.argv)
    except Exception as error:
        print(error)


if __name__ == "__main__":
    main()
