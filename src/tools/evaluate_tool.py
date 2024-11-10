FUNCTION_NAME = "evaluate_user_answer"
FUNCTION_DESC = """\
Call this tool to decide if the answer for the last question is correct.
ALWAYS call this tool ONLY if a question was answered the user said that they already understood the previous explanation.\
"""
OBS_DESC = """\
Some observations about the previous messages that should be considered when evaluating the question.\
"""

evaluate_question_function = {
    "type": "function",
    "function": {
        "name": FUNCTION_NAME,
        "description": FUNCTION_DESC,
        "parameters": {
            "type": "object",
            "properties": {"observations": {"type": "string", "description": OBS_DESC}},
            "required": ["observations"],
        },
    },
}


# TODO
def evaluate_user_answer(*args, **kwargs):
    return kwargs
