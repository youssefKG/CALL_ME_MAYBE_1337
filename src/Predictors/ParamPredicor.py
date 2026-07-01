from src.Enums.JsonState import JsonState


class ParamPredictor:
    def __init__(self, param_type: str) -> None:
        self.param_type: str = self.param_type

    def get_predict_next_tokens(self, json_state: JsonState) -> set[str]:
        res: set[str] = set()
        match self.param_type:
            case "number":
                pass
            case "string":
                pass
            case _:
                pass
        return res
