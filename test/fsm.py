import json
from enum import Enum, auto


class State(Enum):
    START = auto()
    OPEN_OBJECT = auto()
    READ_FUNCTION = auto()
    READ_ARGUMENTS = auto()
    READ_A = auto()
    READ_B = auto()
    ACCEPT = auto()
    ERROR = auto()


class FunctionCallFSM:
    def __init__(self):
        self.state = State.START

    def validate(self, json_string):
        try:
            data = json.loads(json_string)
        except json.JSONDecodeError:
            self.state = State.ERROR
            return False

        # Start
        self.state = State.OPEN_OBJECT

        # Check top-level object
        if not isinstance(data, dict):
            self.state = State.ERROR
            return False

        # Expected keys only
        if set(data.keys()) != {"function", "arguments"}:
            self.state = State.ERROR
            return False

        # Read function
        self.state = State.READ_FUNCTION
        if not isinstance(data["function"], str):
            self.state = State.ERROR
            return False

        # Read arguments
        self.state = State.READ_ARGUMENTS
        args = data["arguments"]

        if not isinstance(args, dict):
            self.state = State.ERROR
            return False

        if set(args.keys()) != {"a", "b"}:
            self.state = State.ERROR
            return False

        # Read a
        self.state = State.READ_A
        if not isinstance(args["a"], (int, float)):
            self.state = State.ERROR
            return False

        # Read b
        self.state = State.READ_B
        if not isinstance(args["b"], (int, float)):
            self.state = State.ERROR
            return False

        # Accept
        self.state = State.ACCEPT
        return True


# ---------------- Example ----------------

json_input = """
{
    "function": "add_numbers",
    "arguments": {
        "a": 40,
        "b": 2
    }
}
"""

fsm = FunctionCallFSM()

if fsm.validate(json_input):
    print("Valid JSON")
    print("Final state:", fsm.state)
else:
    print("Invalid JSON")
    print("Stopped at:", fsm.state)
