from dataclasses import dataclass


@dataclass
class PredictionResult:
    is_found: bool
    possible_predicted_tokens: set[str]
    predicted_token: str
