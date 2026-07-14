from pydantic import BaseModel
from schema_converter import SchemaConverter
import json
import sys
import argparse


class B(BaseModel):
    function_name: str
    parameters: dict[str, str]


def main() -> None:

    parser = argparse.ArgumentParser(
        description="""
            Generates a grammar (suitable for use in ./llama-cli) that produces JSON conforming to a
            given JSON schema. Only a subset of JSON schema features are supported; more may be
            added in the future.
        """,
    )

    parser.add_argument(
        "--raw-pattern",
        type=str,
        help="Treats string patterns as raw patterns w/o quotes (or quote escapes)",
    )

    parser.add_argument("schema", help='file containing JSON schema ("-" for stdin)')
    args = parser.parse_args(sys.argv)
    model_json = json.dumps(B.model_json_schema(), indent=2)
    # args.model_json = model_json
    # schemaConvert = schemaConverter()
    print(args.prop_order)

    print()


main()
