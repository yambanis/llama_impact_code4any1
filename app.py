from dotenv import load_dotenv
load_dotenv()

import os
from crewai import LLM
from flask import Flask, request, g
from twilio.twiml.messaging_response import MessagingResponse
import yaml

from src.flows import FullFlow
from src.db import UserDatabase

import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

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
    if not db.user_exists(request.values.get('From', '')):
        db.create_user(request.values.get('From', ''), request.values.get('ProfileName', ''))
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    test_flow = FullFlow(llm, configs)
    msg = resp.message()
    test_flow._state['message'] = incoming_msg
    msg.body(str(test_flow.kickoff()))
    # msg.media('https://cataas.com/cat')
    return str(resp)


if __name__ == '__main__':
    app.run(port=9000)