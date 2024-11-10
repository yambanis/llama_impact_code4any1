from groq import Groq
from typing import List, Dict
import re


SYSTEM_PROMPT = """\
As an integral part of a programming tutorial chatbot designed to assist
beginners, your task is to perform the onboarding process. Engage with the user
in no more than three interactions to understand what they like and why they
want to learn programming. This information will be used to decide on a suitable
study syllabus.
Once you are satisfied, output
INFORMATION_FOR_SYLLABUS: `content`

This content will be used to generate the study plan.\
"""

def do_onboarding(
    message: str,
    history: List[Dict[str, str]],
    client: Groq,
):

    # Change system prompt to fit the intention of a final response.
    if len(history) > 0 and history[0]["role"] == "system":
        history[0] = {"role": "system", "content": SYSTEM_PROMPT}
    else:
        history = [{"role": "system", "content": SYSTEM_PROMPT}] + history

    new_message = [{"role": "user", "content": message}]
    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile", messages=history + new_message
    )
    output_response = response.choices[0].message.content

    pattern = r'INFORMATION_FOR_SYLLABUS:\s*(.*?)$'
    match = re.search(pattern, output_response, re.MULTILINE)
    information_for_syllabus = match.group(1) if match else None
    output_response = output_response.replace("INFORMATION_FOR_SYLLABUS:", "")
    if information_for_syllabus:
        output_response = output_response.replace(information_for_syllabus, "")
    
    return output_response, information_for_syllabus, history + new_message
