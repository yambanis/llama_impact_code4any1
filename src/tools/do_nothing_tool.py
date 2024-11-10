QUESTION_FUNCTION_NAME = "do_nothing_function"
QUESTION_FUNCTION_DESC = """\
If you feel like you don't need to call a function.\
"""

do_nothing_function = {
    "type": "function",
    "function": {
        "name": "",
        "description": QUESTION_FUNCTION_DESC,
        "parameters": {},
        "required": [],
    },
}
