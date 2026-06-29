from src.Enums.ModelState import ModelState
from src.Parser.Parser import Parser
from src.Prompts.Prompt import Prompt
from src.LlmModel.model import Model


def main() -> None:
    model: Model = Model()
    # parser: Parser = Parser(sys.argv)
    # parser.parse()
    # promt: Prompt = Prompt(parser.get_functions_defintions)
    # promt_str: str = promt.generate(
    #     user_prompt="What is the sum of 2 and 3?",
    #     model_state=ModelState.SelectingFunctionName,
    # )
    # print(promt_str)


if __name__ == "__main__":
    main()
