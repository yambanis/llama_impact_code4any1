import json
from typing import Any

from groq import Groq
from retrying import retry

from src.tools import (
    do_nothing_tool,
    evaluate_tool,
    question_tool,
    topic_tool,
    update_state_tool,
)

SYSTEM_PROMPT = """\
You are part of a system that teaches programming.
Choose the function that fits best the next user message.
"""

TOOLS = [
    topic_tool.create_explanation_function,
    do_nothing_tool.do_nothing_function,
    question_tool.create_question_function,
    evaluate_tool.evaluate_question_function,
    update_state_tool.update_curriculum_function,
]

WEIGHTS = {
    tool.function["name"]: (
        float("-inf")
        if tool["function"]["name"] == do_nothing_tool.FUNCTION_NAME
        else 1.0
    )
    for tool in TOOLS
}

TOOLS_IMPLEMENTATION = {
    topic_tool.FUNCTION_NAME: topic_tool.explain_topic,
    question_tool.FUNCTION_NAME: question_tool.create_topic_question,
    evaluate_tool.FUNCTION_NAME: evaluate_tool.evaluate_user_answer,
    update_state_tool.FUNCTION_NAME: update_state_tool.update_curriculum,
    do_nothing_tool.FUNCTION_NAME: do_nothing_tool.do_nothing,
}


@retry(stop_max_attempt_number=5, wait_fixed=100)
def execute_router(
    new_message: str,
    history: list[dict[str, str]],
    client: Groq,
    tools: list[dict[str, Any]],
    weights: dict[str, float],
    model: str = "llama3-groq-70b-8192-tool-use-preview",
):
    if history[0]["role"] == "system":
        history[0] = {"role": "system", "content": SYSTEM_PROMPT}
    else:
        history = {"role": "system", "content": SYSTEM_PROMPT} + history

    tool_names = [tool["function"]["name"] for tool in tools]
    chat_completion = client.chat.completions.create(
        messages=history + [{"role": "user", "content": new_message}],
        model=model,
        tools=tools,
        tool_choice="required",
    )

    # If len is less than 1, this raises an error and triggers retry.
    tool_calls = sorted(
        [
            (call, WEIGHTS[call.function.name])
            for call in chat_completion.choices[0].message.tool_calls
            if call.function.name in tool_names
        ],
        key=lambda x: x[1],
    )

    if tool_calls:
        (tool_call, _), *_ = tool_calls
        return tool_call

    else:
        raise ValueError()


# nao sei typar pq nao rodei rs
def execute_tool_call(tool_call: Any) -> Any:
    args = json.loads(tool_call.function.arguments)
    function_to_call = TOOLS_IMPLEMENTATION[tool_call.function.name]
    tool_response = function_to_call(**args)

    return tool_response
