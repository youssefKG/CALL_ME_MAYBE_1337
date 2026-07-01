from src.Enums.JsonState import JsonState
from src.Enums.ModelState import ModelState


class Generator:
    def __init__(self) -> None:
        self.json_state: JsonState = JsonState.START
        self.model_state: ModelState = ModelState.SelectingFunctionName

    def predict_next_json_token(self) -> str:
        match self.json_state:
            case JsonState.START:
                return '"'
            case JsonState.STRING:
                return (
                    " !#$%&'()*+,-./0123456789:;<=>?@"
                    "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
                    "[^_`"
                    "abcdefghijklmnopqrstuvwxyz"
                    "{|}~"
                )
            case _:
                return ""
