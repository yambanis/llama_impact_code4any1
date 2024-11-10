import json
from groq import Groq
from retrying import retry

from tools import topic_tool, do_nothing, question_tool, evaluate_tool

SYSTEM_PROMPT = """\
You are part of a system that teaches programming.
Choose the function that fits best the next user message.\
"""

# TODO: Add other tools.
TOOL_NAMES = [
    topic_tool.create_explanation_function,
    do_nothing.do_nothing_function,
    question_tool.create_question_function,
    evaluate_tool.evaluate_question_function,
]
TOOLS = [tool["function"]["name"] for tool in TOOL_NAMES]
WEIGHTS = {
    "response_without_tools": float("-inf"),
    "create_topic_explanation": 1.0,
}
TOOLS_IMPLEMENTATION = {
    topic_tool.EXPLAIN_FUNCTION_NAME: topic_tool.create_explanation, 
    question_tool.QUESTION_FUNCTION_NAME: question_tool.create_explanation, 
    evaluate_tool.EVALUATE_FUNCTION_NAME: evaluate_tool.create_explanation, 
}


@retry(stop_max_attempt_number=5, wait_fixed=100)
def execute_router(
    new_message: str,
    history: list[dict[str, str]],
    client: Groq,
):

    # Change system prompt to fit the intention of a final response.
    if history[0]["role"] == "system":
        history[0] = {"role": "system", "content": SYSTEM_PROMPT}
    else:
        history = {"role": "system", "content": SYSTEM_PROMPT} + history


    chat_completion = client.chat.completions.create(
        messages= history + [{"role": "user", "content": new_message}],
        model="llama3-groq-70b-8192-tool-use-preview",
        tools=TOOLS,
        tool_choice="required",
    )

    # If len is less then 1, this raises an error and triggers retry.
    tool_calls = sorted(
        [
            (call, WEIGHTS[call.function.name])
            for call in chat_completion.choices[0].message.tool_calls
            if call.function.name in TOOLS
        ],
        key=lambda x: x[1],
    )

    if tool_calls:
        (tool_call, _), *_ = tool_calls
        return tool_call

    else:
        raise ValueError()


def execute_tool_call(tool_call):
    args = json.loads(tool_call.function.arguments)

    if tool_call.function.name == "do_nothing":
        tool_response = "nothing"
    else:
        function_to_call = TOOLS_IMPLEMENTATION[tool_call.function.name]
        tool_response = function_to_call(**args)

    return tool_response
