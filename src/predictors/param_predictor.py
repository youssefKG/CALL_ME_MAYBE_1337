from Models.FunctionDefinitionJson import FunctionDefinitionModel
from src.Enums.JsonState import JsonState
from .prediction_result import PredictionResult

NUMERIC_TOKENS: set[str] = set(
    {"+", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9", "."}
)


class ParamPredictor:
    def __init__(self, fn: FunctionDefinitionModel) -> None:
        self.fn: FunctionDefinitionModel = fn

    def predict(self, param_type: str, pregenerate_param: str) -> set[str]:
        predicted_tokens: set[str] = set({})
        if param_type == "number":
            return NUMERIC_TOKENS
        elif param_type == "string":
            return set({})
        return predicted_tokens
