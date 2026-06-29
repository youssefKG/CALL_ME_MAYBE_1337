from enum import Enum


class PromptType(str, Enum):
    FUNCTION_NAME = """
    You are a function selector.

    Functions:
    {FUNCTIONS}

    Task:

    Read the user request.
    Choose the function whose description best matches the request.
    Return ONLY the function name.
    Do not explain.
    Do not output JSON.
    Do not output any other text.

    Examples:

    User: What is the sum of 2 and 3?
    Output: fn_add_numbers

    User: Greet John
    Output: fn_greet

    User: Reverse hello
    Output: fn_reverse_string

    User:
    {USER_PROMPT}

    Output: """

    FUNCTION_ARGUMENT = """
    You are a parameter extractor.

    The function has already been selected.

    Function:

    {FUNCTION}

    User request:

    {USER_PROMPT}

    Task:

    * Extract the arguments for this function.
    * Use the exact parameter names.
    * Use the correct parameter types.
    * Return ONLY a JSON object containing the parameters.
    * Do not include the function name.
    * Do not explain.
    * Do not output any other text.

    Examples:

    Function:
    fn_add_numbers(a: number, b: number)

    User:
    What is the sum of 2 and 3?

    Output:
    {"a":2,"b":3}

    Function:
    fn_greet(name: string)

    User:
    Greet John

    Output:
    {"name":"John"}

    Function:
    {FUNCTION}

    User:
    {USER_PROMPT}

    Output:
    """
