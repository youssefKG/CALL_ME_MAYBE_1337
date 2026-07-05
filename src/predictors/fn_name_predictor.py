from .predictor_utils import  Trie


class FnNamePredictor:


    def __init__(self, fns_names_ids: list[list[int]]) -> None:
        self.__fns_names_ids: list[list[int]] = fns_names_ids
        self.__fns_names_ids_trie: Trie = Trie()
        self.__set_fns_names_ids_trie()

    def __set_fns_names_ids_trie(self) -> None:
        for fn_ids in self.__fns_names_ids:
            self.__fns_names_ids_trie.add(fn_ids)

    def get_next_predictions_ids(self, ids: list[int]) -> list[int]:
        return self.__fns_names_ids_trie.get_children(ids)

    def is_completed(self, ids: list[int]) -> bool:
        return self.__fns_names_ids_trie.search(ids)



def test_fn_names_predictor() -> None:
    test_one: list[list[int]] = [[1, 2, 3, 4, 5, 6, 10], [1, 2, 3, 4, 5, 6, 9, 10], [1, 2, 3, 4, 5, 6, 7, 8],[1, 2, 3, 4, 5, 6, 17, 8]]
    fn_names_predictor: FnNamePredictor = FnNamePredictor(test_one)
    print(fn_names_predictor.get_next_predictions_ids([1, 2, 3, 4, 5, 6]))
    print(fn_names_predictor.is_completed([1, 2, 3, 4, 5, 6, 10]))


if __name__ == "__main__":
    test_fn_names_predictor()

"""


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
"""


# TEST
"""

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
"""
