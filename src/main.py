from llm_sdk.llm_sdk import Small_LLM_Model
from torch import Tensor


def main() -> None:
    llm_model = Small_LLM_Model()
    encoded_data: Tensor = llm_model.encode("whats the name of youssef")
    list_encoded_data = encoded_data.tolist()[0]
    print(llm_model.get_logits_from_input_ids(list_encoded_data))


main()
