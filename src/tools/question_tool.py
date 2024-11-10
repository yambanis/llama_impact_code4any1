FUNCTION_NAME = "create_topic_question"
FUNCTION_DESC = """\
Call this tool to create a question for the user about the last topic.
ALWAYS call this tool ONLY if the user said that they already understood the previous explanation.\
"""
OBS_DESC = """\
Some observations about the previous messages that should be considered when writing the question.\
"""

create_question_function = {
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
def create_topic_question(*args, **kwargs):
    return kwargs
