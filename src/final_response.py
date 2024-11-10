from groq import Groq
from typing import List, Dict


SYSTEM_PROMPT = """\
You are an integral part of a programming tutorial chatbot designed to assist
beginners. As the final layer of user interaction, your role is to provide clear
and helpful responses that the user will see directly. Our system has
preprocessed data and will supply you with relevant details about useful tools
to guide your answers and improve the learning experience for the user.\
"""

# client = Groq(api_key="...")
# Não sei se a gente quer passar o history já nesse formato que o modelo espera.
def chat_final_response(
    tool_used: str,
    tool_observation: str,
    history: List[Dict[str, str]],
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
        new_message = []

    response = client.chat.completions.create(
        model="llama-3.1-70b-versatile", messages=history + new_message
    )
    return response.choices[0].message


# Exemplo de uso :D
# messages = [
#     {"role": "system", "content": """You are a helpful assistant."""},
#     {
#         "role": "user",
#         "content": "What is the price for a cappuccino and croissant?",
#     },
#     {
#         "role": "assistant",
#         "content": "Sei lá!! XD",
#     },
#     {
#         "role": "user",
#         "content": "Me ajuda com if. O que é isso?",
#     },
# ]

# tool_used = "topic_explanation"
# tool_observation = """An `if-else` statement is a conditional structure in programming used to make decisions based on a condition.

# 1. **If Condition**: It checks if a specified condition is true.
# 2. **Code Execution**: If the condition is true, the code block under `if` runs.
# 3. **Else Statement**: If the condition is false, the `else` block executes.
# 4. **Alternative Conditions**: You can add multiple conditions using `elif` in some languages.
# 5. **End of Statement**: Only one block runs based on the first true condition."""

# chat_final_response(tool_used=tool_used, tool_observation=tool_observation, history=messages, client=client)
# >>> ChatCompletionMessage(content='Ah, sim. Basicamente o "if" permite que você determine fluxos de execução diferente do código dependendo de certos estados iniciais. Por exemplo, se um valor é igual a outro, maior ou menor. Se uma condição é atendida, você pode especificar que corpos de código venham a ser adotados.\n\nVamos com um exemplo básico com Python:\n\n```python\nx = 10\nif x > 5:\n   print("x é maior que 5")\n```\n\nEm Python, a sintaxe `if` também pode ter expressões `elif` e `else`, que estão associadas a condições e corpos de códigos.\n\nO exemplo acima é muito direto. Quando você ter várias condições a serem atendidas antes de tomar um corpo de ação, o uso de `elif` e/ou `else` deve ser imperativo. \n\nA lista abaixo utiliza o exemplo anterior e melhorado no bloco de códigos aqui.\n\n*   `if`: condição (True ou False). Executa o corpo de código se verdadeiro.\n*   `elif`: Executar condição, após avaliar a condição `if` e tendo resultado falso. Também executa corpo de código se verdadeiro.\n\n```python\n# Declaro a váriavel e imprimo\nx = 10\nprint("Declaração de x: ", x)\n\n# Verificao de condições\nif x == 0:\n   print("x é igual a zero.")\nelif x > 0:\n   print("x é maior que zero.")\nelif x < 0:\n   print("x é menor que zero.")\nelse:\n   print("Declaração inválida de valor.")\n```\n\nExistem mais contextos na linguagem para utilizar-se do operador lógico `if`, inclusive no contexto de matérias avançadas.', role='assistant', function_call=None, tool_calls=None)