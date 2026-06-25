class Prompt:
    def __init__(self, functions_calls: str) -> None:
        self.prompt_template: str =
        """
        You are a function caller.
        Functions:
        {FUNCTIONS}

        Rules:

        * Choose exactly one function.
        * Match the request to the function description.
        * Extract all parameters.
        * Use exact parameter names and types.
        * Output JSON only.
        * No explanation.

        Examples:

        User: What is the sum of 2 and 3?
        Output: {"name":"fn_add_numbers","parameters":{"a":2,"b":3}}

        User: Greet John
        Output: {"name":"fn_greet","parameters":{"name":"John"}}

        User: Reverse hello
        Output: {"name":"fn_reverse_string","parameters":{"s":"hello"}}

        User: {USER_PROMPT}
        Output:
        """.replace("{FUNCTIONS}", functions_calls)


    def generate(self, user_prompt: str) -> str:
        return self.prompt_template.replace("{USER_PROMPT}", user_prompt)


