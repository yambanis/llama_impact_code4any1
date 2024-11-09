from dotenv import load_dotenv
load_dotenv()

import os
from crewai import LLM
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import yaml

from src.flows import FullFlow

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

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

test_flow = FullFlow(llm, configs)

@app.route('/message', methods=['POST'])
def message():
    print(request.get_data())
    incoming_msg = request.values.get('Body', '').lower()
    resp = MessagingResponse()
    msg = resp.message()
    test_flow.state['user_input'] = incoming_msg
    msg.body(str(test_flow.kickoff()))
    # msg.media('https://cataas.com/cat')
    return str(resp)


if __name__ == '__main__':
    app.run(port=9000)