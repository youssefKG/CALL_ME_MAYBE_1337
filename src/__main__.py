from src.llm_model.model import Model


def main() -> None:
    model = Model()
    print(model.get_next_token("say hi: ?"))


if __name__ == "__main__":
    main()
