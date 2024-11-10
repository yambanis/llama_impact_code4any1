from groq import Groq

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

SYSTEM_PROMPT = f"""\
You are an integral part of a programming tutorial chatbot designed to assist
beginners. Your role is to evaluate if the provided answer for the last question is correct.
Write a message that says if the message is correct and a short explanation of why.
Take into account that the user is a beginner in programming, so use a simple language.\
"""


def evaluate_user_answer(history: list[dict[str, str]], client: Groq):
    if not history:
        raise ValueError

    # Change system prompt to fit the intention of a final response.
    if history[0]["role"] == "system":
        history[0] = {"role": "system", "content": SYSTEM_PROMPT}
    else:
        history = {"role": "system", "content": SYSTEM_PROMPT} + history

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile", messages=history
    )
    return response.choices[0].message.content, history + [
        {"role": "assistant", "content": response.choices[0].message.content}
    ]