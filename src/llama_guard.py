from groq import Groq


# client = Groq(api_key=os.getenv('GROQ_API_KEY'))
def get_is_safe_llamaguard_response(client: Groq, user_message: str) -> bool:
    chat_completion = client.chat.completions.create(
        messages=[
            {
                "role": "user",
                "content": user_message
            }
        ],
        model="llama-guard-3-8b",
    )
    return chat_completion.choices[0].message.content.startswith("safe")
