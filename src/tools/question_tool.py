QUESTION_FUNCTION_NAME = "create_topic_question"
QUESTION_FUNCTION_DESC = """\
Call this tool to create a question for the user about the last topic.
ALWAYS call this tool ONLY if the user said that they already understood the previous explanation.\
"""
QUESTION_OBS_DESC = """\
Some observations about the previous messages that should be considered when writing the question.\
"""

create_question_function = {
    "type": "function",
    "function": {
        "name": QUESTION_FUNCTION_NAME,
        "description": QUESTION_FUNCTION_DESC,
        "parameters": {
            "type": "object",
            "properties": {
                "observations": {"type": "string", "description": QUESTION_OBS_DESC}
            },
            "required": ["observations"],
        },
    },
}

def create_question(*args, **kwargs):
    pass
    # TODO: Call algum crew AI do Gui
    # Maybe we want to add the params of history and of user information(?)
    # Probably inside the flow itself.
