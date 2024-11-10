FUNCTION_NAME = "call_no_tool"
FUNCTION_DESC = """\
ALWAYS call this tool ONLY if no tool can be called based on the last user message.\
"""

do_nothing_function = {
    "type": "function",
    "function": {
        "name": FUNCTION_NAME,
        "description": FUNCTION_DESC,
        "parameters": {},
        "required": [],
    },
}

def do_nothing(*args, **kwargs):
    return "preguiça de responderkkkkkkkkkj"