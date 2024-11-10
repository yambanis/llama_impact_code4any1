from dotenv import load_dotenv
load_dotenv()

import os
from flask import Flask, request, g
from groq import Groq
import json
from twilio.twiml.messaging_response import MessagingResponse

from src.db import UserDatabase
from src.onboarding_chat import do_onboarding
from src.llama_guard import get_is_safe_llamaguard_response
from src.curriculum import CurriculumFlow
from src.tool_router import execute_router, execute_tool_call
from src.final_response import chat_final_response
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)
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
                db.update_user_context(user_id, information_for_syllabus)
                print("User is onboarded")
                curriculum_flow = CurriculumFlow()
                curriculum_flow._state['message'] = db.get_user_context(user_id)
                curriculum_message = curriculum_flow.kickoff()
                db.update_curriculum(user_id, str(curriculum_message))

            out = str(response_message)
        
        else:
            try:
                tool_call = execute_router(incoming_msg, memory, client)
                out = execute_tool_call(tool_call)
                out, history = chat_final_response(tool_call.function.name, out, memory, client)
                db.update_memory(user_id, json.dumps(history))
            except ValueError:
                out = "Ops, não entendi o que você disse."

    resp = MessagingResponse()
    msg = resp.message()
    msg.body(out)
    return str(resp)


if __name__ == '__main__':
    app.run(port=9000)
