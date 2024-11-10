from dotenv import load_dotenv
load_dotenv()

import os
from crewai import LLM
from flask import Flask, request, g
from groq import Groq
import json
from twilio.twiml.messaging_response import MessagingResponse
import yaml

from src.flows import FullFlow
from src.db import UserDatabase
from src.onboarding_chat import do_onboarding
from src.llama_guard import get_is_safe_llamaguard_response

import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
llm = LLM(
    model="groq/llama-3.1-70b-versatile", 
    api_key=os.getenv("GROQ_API_KEY")
)
# Define file paths for YAML configurations
files = {
    'agents': 'configs/agents.yaml',
    'tasks': 'configs/tasks.yaml'
}

# Replace the global db instance with a function to get db connection
def get_db():
    if 'db' not in g:
        g.db = UserDatabase("users.db")
    return g.db

@app.teardown_appcontext
def close_db(error):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

@app.route('/message', methods=['POST'])
def message():
    db = get_db()  # Get thread-local database connection
    user_id = request.values.get('From', '')
    incoming_msg = request.values.get('Body', '').lower()

    is_safe = get_is_safe_llamaguard_response(client, incoming_msg)
    if not is_safe:
        print("Message is not safe")
        out = "Desculpe, não posso responder a isso."
    else:
        out = ""
        if not db.user_exists(user_id):
            db.create_user(user_id, request.values.get('ProfileName', ''))
        memory = db.get_memory(user_id)
        if not memory:
            memory = "[]"
        memory = json.loads(memory)
        if not db.user_onboarded(user_id):
            response_message, information_for_syllabus, history = do_onboarding(incoming_msg, memory, client)
            db.update_memory(user_id, json.dumps(history))

            if information_for_syllabus:
                db.user_is_onboarded(user_id)
                print("User is onboarded")
            out = str(response_message)

        else:
            out = "nothing yet"
    
    # tool_use = decide_tool(message, memory, ementa) # esqueleto que temos
    # observacao_tool = use tool # esqueleto que temos
    # response_message = chat_response(message, memory, tool_use, observacao_tool)
    # guardar interação na memória
    # return str(response_message)


    


    # test_flow = FullFlow(llm, configs)
    # test_flow._state['message'] = incoming_msg

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(out)
    # msg.media('https://cataas.com/cat')
    return str(resp)


if __name__ == '__main__':

    app.run(port=9000)