FUNCTION_NAME = "explain_topic"
FUNCTION_DESC = """\
Call this tool to explain a programming topic for the user.
Takes into account previous explanations in order to write clearer explanations, if the topic has already been explained before.\
"""
OBS_DESC = """\
Some observations about the previous messages that should be considered when writing the explanation.\
"""

create_explanation_function = {
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


# TODO: Definir o observation no flow
# TODO: Pegar o tópico do state e definir no flow
def explain_topic(flow, *args, **kwargs):
    return flow.kickoff()
