from crewai import Flow
from crewai.flow.flow import listen, start
from crewai import Agent, Task, Crew
from src.base_crewai_config import llm, agents_config, tasks_config


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
        return {
            'user_persona': self.state['user_persona'],
            'curriculum': self.state['curriculum']
        }
    
    @listen(fetch_user_info)
    def question_creation(self, inputs):
        question = question_crew.kickoff(inputs=inputs)    
        return question
