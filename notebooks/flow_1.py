# Warning control
import warnings
warnings.filterwarnings('ignore')

import os
import yaml
from crewai import Agent, Task, Crew
from crewai import LLM

llm = LLM(
    model="groq/llama-3.1-70b-versatile", 
    api_key="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"
)
# Define file paths for YAML configurations
files = {
    'agents': '../configs/basic_config/agents.yaml',
    'tasks': '../configs/basic_config/tasks.yaml'
}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']
# Creating Agents
onboarding_agent = Agent(
  config=agents_config['onboarding_agent'],
  llm=llm,
  human_input=True
)

question_creation_agent = Agent(
  config=agents_config['question_creation_agent'],
  llm=llm
)

# Creating Tasks
user_onboarding = Task(
  config=tasks_config['user_onboarding'],
  agent=onboarding_agent
)

question_creation = Task(
  config=tasks_config['question_creation'],
  agent=question_creation_agent,
)

question_critic = Task(
  config=tasks_config['question_critic'],
  agent=question_creation_agent,
)

onboarding_crew = Crew(
  agents=[
    onboarding_agent
  ],
  tasks=[
    user_onboarding
  ],
  verbose=True
)

question_crew = Crew(
  agents=[
    question_creation_agent
  ],
  tasks=[
    question_creation,
    question_critic
  ],
  verbose=True
)

from crewai import Flow
from crewai.flow.flow import listen, start

class onboardingFlow(Flow):
    @start()
    def fetch_user(self):
        user_input = {
            'user_input': input()
        }
        return user_input

    @listen(fetch_user)
    def onboarding(self, user_input):
        user_info = onboarding_crew.kickoff(inputs=user_input)
        with open('state.txt', 'w') as f:
            f.write(str(user_info))

        return user_info


class questionFlow(Flow):
    @start()
    def fetch_user_info(self):
        with open('state.txt', 'r') as f:
            user_persona = f.read()
        self.state['user_persona'] = user_persona  

        return user_persona
    
    @listen(fetch_user_info)
    def question_creation(self, user_persona):
        question = question_crew.kickoff(inputs={'user_persona': user_persona})
    
        return question

oflow = onboardingFlow()
oflow.kickoff()

qflow = questionFlow()
qflow.kickoff()