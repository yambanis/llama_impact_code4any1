FUNCTION_NAME = "update_curriculum"
FUNCTION_DESC = """\
Call this tool to update the curriculum.
ALWAYS call this tool ONLY if the user answered the last question correctly.\
"""
OBS_DESC = """\
Some observations about the previous messages that should be considered when updating the curriculum.\
"""

update_curriculum_function = {
    "type": "function",
    "function": {
        "name": FUNCTION_NAME,
        "description": FUNCTION_DESC,
        "parameters": {
            "type": "object",
            "required": ["observations"],
            "properties": {"observations": {"type": "string", "description": OBS_DESC}},
        },
    },
}


# TODO: Pegar o tópico do state e definir no flow
# TODO: Atualizar o status do tópico no state
def update_curriculum(*args, **kwargs):
    return "Essa mensagem significa que o agente está atualizando a ementa"
