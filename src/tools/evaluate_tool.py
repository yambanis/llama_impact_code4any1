EVALUATE_FUNCTION_NAME = "evaluate_user_answer"
EVALUATE_FUNCTION_DESC = """\
Call this tool to decide if the answer for the last question is correct.
ALWAYS call this tool ONLY if a question was answered the user said that they already understood the previous explanation.\
"""
EVALUATE_OBS_DESC = """\
Some observations about the previous messages that should be considered when writing the question.\
"""

evaluate_question_function = {
    "type": "function",
    "function": {
        "name": EVALUATE_FUNCTION_NAME,
        "description": EVALUATE_FUNCTION_DESC,
        "parameters": {
            "type": "object",
            "properties": {
                "observations": {"type": "string", "description": EVALUATE_OBS_DESC}
            },
            "required": ["observations"],
        },
    },
}

def evaluate_question():
    pass
    # TODO: Call algum crew AI do Gui
    # Maybe we want to add the params of history and of user information(?)
    # Probably inside the flow itself.
