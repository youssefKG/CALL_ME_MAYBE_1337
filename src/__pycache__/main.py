from llm_sdk.llm_sdk import Small_LLM_Model


def main() -> None:

    llm_model = Small_LLM_Model()
    _ = llm_model.encode("hello world")


main()
