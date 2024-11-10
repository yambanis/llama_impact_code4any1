EXPLAIN_FUNCTION_NAME = "explain_topic"
EXPLAIN_FUNCTION_DESC = """\
Creates an explanation for a programming topic for the user.
Takes into account previous explanations in order to write clearer explanations, if the topic has already been explained before.\
"""
EXPLAIN_OBS_DESC = """\
Some observations about the previous messages that should be considered when writing the explanation.\
"""

create_explanation_function = {
    "type": "function",
    "function": {
        "name": EXPLAIN_FUNCTION_NAME,
        "description": EXPLAIN_FUNCTION_DESC,
        "parameters": {
            "type": "object",
            "properties": {
                "observations": {"type": "string", "description": EXPLAIN_OBS_DESC}
            },
            "required": ["observations"],
        },
    },
}


def create_explanation():
    pass
    # TODO: Call algum crew AI do Gui
    # Maybe we want to add the params of history and of user information(?)
    # Probably inside the flow itself.
