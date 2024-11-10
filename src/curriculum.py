from crewai import Flow
from crewai.flow.flow import listen, start
from crewai import Agent, Task, Crew
from src.base_crewai_config import llm, agents_config, tasks_config
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


class CurriculumFlow(Flow):
    @start()
    def fetch_user_info(self):
        user_input = {
            'user_persona': self.state['message'],
        }

        self.state.update(user_input)

        return user_input
    
    @listen(fetch_user_info)
    def guidance(self, user_input):
        curriculum_message = help_crew.kickoff(inputs=user_input)    
        return curriculum_message