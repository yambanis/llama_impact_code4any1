from crewai import Flow
from crewai.flow.flow import listen, start
from crewai import Agent, Task, Crew
from llama_impact_code4any1.crews.base_config import llm, agents_config, tasks_config


question_creation_agent = Agent(
  config=agents_config['question_creation_agent'],
  llm=llm
)

question_creation = Task(
  config=tasks_config['question_creation'],
  agent=question_creation_agent,
)

question_critic = Task(
  config=tasks_config['question_critic'],
  agent=question_creation_agent,
)


question_crew = Crew(
  agents=[
    question_creation_agent
  ],
  tasks=[
    question_creation,
    question_critic
  ],
  verbose=False
)

class questionFlow(Flow):
    @start()
    def fetch_user_info(self):
        with open('user_persona.txt', 'r') as f:
            user_persona = f.read()
        self.state['user_persona'] = user_persona  

        return user_persona
    
    @listen(fetch_user_info)
    def question_creation(self, user_persona):
        question = question_crew.kickoff(inputs={'user_persona': user_persona})

        with open('user_messages.txt', 'w+') as f:
            f.write(str(question))
    
        return question