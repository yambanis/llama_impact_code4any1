from groq import Groq
from typing import List, Dict
import re


SYSTEM_PROMPT = """\
As an integral part of a programming tutorial chatbot designed to assist
beginners, your task is to perform the onboarding process. 

Engage with the user in no more than three interactions to understand what they like and why they
want to learn programming. This information will be used to decide on a suitable study syllabus.

If the conversation is dragging, your the user says something like "Looks good", "Let's get started" etc, 
output the final result,

Here is the format you must output:

# USER INFORMATION
## Persona
## Interests
## Knowledge level

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

    pattern = r'USER INFORMATION\s*(.*?)$'
    match = re.search(pattern, output_response, re.MULTILINE)
    information_for_syllabus = match.group(1) if match else None

    # if information_for_syllabus:
    #     pattern = r'INFORMAÇÃO PARA CURRÍCULO:\s*(.*?)$'
    #     match = re.search(pattern, output_response, re.MULTILINE)
    #     information_for_syllabus = match.group(1) if match else None

    output_response = output_response.replace("USER INFORMATION:", "")

    if information_for_syllabus:
        output_response = output_response.replace(information_for_syllabus, "")
    
    return output_response, information_for_syllabus, history + new_message + [{"role": "assistant", "content": output_response}]
