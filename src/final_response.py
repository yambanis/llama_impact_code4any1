from typing import Dict, List

from groq import Groq

SYSTEM_PROMPT = """\
You are an integral part of a programming tutorial chatbot designed to assist
beginners. As the final layer of user interaction, your role is to provide clear
and helpful responses that the user will see directly. Our system has
preprocessed data and will supply you with relevant details about useful tools
to guide your answers and improve the learning experience for the user.
Always answer in the same language of the user.\
"""

# client = Groq(api_key="...")
# Não sei se a gente quer passar o history já nesse formato que o modelo espera.
def chat_final_response(
    tool_used: str,
    tool_observation: str,
    history: List[Dict[str, str]],
    message: str,
    client: Groq,
):
    if not history:
        raise ValueError

    # Change system prompt to fit the intention of a final response.
    if history[0]["role"] == "system":
        history[0] = {"role": "system", "content": SYSTEM_PROMPT}
    else:
        history = {"role": "system", "content": SYSTEM_PROMPT} + history

    if tool_used != "do_nothing":
        new_message = [
            {
                "role": "tool",
                "tool_call_id": tool_used,
                "content": str(tool_observation),
            }
        ]
    else:
        new_message = [{"role": "user", "content": message}]

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile", messages=history + new_message
    )
    return response.choices[0].message.content, history + new_message + [{"role": "assistant", "content": response.choices[0].message.content}]
