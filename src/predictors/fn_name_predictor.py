from .prediction_result import PredictionResult


class FnNamePredictor:
    def __init__(self, functions_names: set[str]) -> None:
        self.functions_names: set[str] = functions_names

    def predict(self, pre_generate_name: str) -> PredictionResult:
        next_predicted_tokens: set[str] = set({})
        fn_names_that_start_with_pregenerated: set[str] = (
            self.__fn_names_that_start_with_pregenerated_name(pre_generate_name)
        )
        if len(fn_names_that_start_with_pregenerated) == 1:
            predicted_fn_name: str = fn_names_that_start_with_pregenerated.pop()
            return PredictionResult(
                is_found=True,
                possible_predicted_tokens=next_predicted_tokens,
                predicted_token=predicted_fn_name,
            )
        next_predicted_tokens = self.__get_predicted_tokens(
            pre_generate_name, fn_names_that_start_with_pregenerated
        )
        return PredictionResult(
            is_found=False,
            possible_predicted_tokens=next_predicted_tokens,
            predicted_token="",
        )

    def __fn_names_that_start_with_pregenerated_name(
        self, pre_generate_name: str
    ) -> set[str]:
        fn_names: set[str] = set({})
        for fn_name in self.functions_names:
            if fn_name.startswith(pre_generate_name):
                fn_names.add(fn_name)
        return fn_names

    def __get_predicted_tokens(
        self, pre_generated_name: str, fn_names: set[str]
    ) -> set[str]:
        tokens: set[str] = set({})
        for fn_name in fn_names:
            idx: int = fn_name.index(pre_generated_name[-1])
            if idx < len(fn_name) - 1:
                tokens.add(fn_name[idx + 1])
        return tokens


# TEST
def test_predirect_token_for_fn_names(pregenerated_fn_name: str) -> None:
    fn_names: set[str] = set(
        {
            "fn_add_numbers",
            "fn_greet",
            "fn_reverse_string",
            "fn_get_square_root",
            "fn_substitute_string_with_regex",
        }
    )
    fn_name_precdictor: FnNamePredictor = FnNamePredictor(fn_names)
    prediction_result: PredictionResult = fn_name_precdictor.predict(
        pregenerated_fn_name
    )
    if prediction_result.is_found:
        print(f"the function name is found: {prediction_result.predicted_token}")
    else:
        print(f"next predicted tokens: {prediction_result.possible_predicted_tokens}")


if __name__ == "__main__":
    test_predirect_token_for_fn_names("fn_")
    test_predirect_token_for_fn_names("f")
