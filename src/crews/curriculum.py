from crewai import Flow
from crewai.flow.flow import listen, start
from crewai import Agent, Task, Crew
from llama_impact_code4any1.crews.base_config import llm, agents_config, tasks_config
from crewai_tools import SerperDevTool

curriculum_builder = Agent(
  config=agents_config['curriculum_builder'],
  llm=llm
)

search_tool = SerperDevTool()

create_curriculum = Task(
    config=tasks_config['create_curriculum'],
    agent=curriculum_builder,
    tools=[search_tool]
)

help_crew = Crew(
  agents=[
    curriculum_builder
  ],
  tasks=[
    create_curriculum
  ],
  verbose=False
)


class curriculumFlow(Flow):
    @start()
    def fetch_user_info(self):
        with open('user_persona.txt', 'r') as f:
            user_persona = f.read()
        
        user_input = {
            'user_persona': user_persona,
        }

        self.state.update(user_input)

        return user_input
    
    @listen(fetch_user_info)
    def guidance(self, user_input):
        curriculum_message = help_crew.kickoff(inputs=user_input)
    
        with open('curriculum.txt', 'w+') as f:
            f.write(str(curriculum_message))
        
        return curriculum_message