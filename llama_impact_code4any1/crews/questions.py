from crewai import Agent, Crew, Flow, Task
from crewai.flow.flow import listen, start
from src.crews.base_config import agents_config, llm, tasks_config

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
        with open('curriculum.txt', 'r') as f:
            curriculum = f.read()
        self.state['curriculum'] = curriculum  

        return {
            'user_persona': user_persona,
            'curriculum': curriculum
        }
    
    @listen(fetch_user_info)
    def question_creation(self, inputs):
        question = question_crew.kickoff(inputs=inputs)

        with open('user_messages.txt', 'w+') as f:
            f.write(str(question))
    
        return question