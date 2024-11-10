from crewai import Agent, Crew, Flow, Task
from crewai.flow.flow import listen, start
from crewai_tools import SerperDevTool
from src.crews.base_config import agents_config, llm, tasks_config

question_creation_agent = Agent(
  config=agents_config['question_creation_agent'],
  llm=llm
)

search_tool = SerperDevTool()

teaching_help = Task(
    config=tasks_config['teaching_help'],
    agent=question_creation_agent,
    tools=[search_tool]
)

help_crew = Crew(
  agents=[
    question_creation_agent
  ],
  tasks=[
    teaching_help
  ],
  verbose=False
)


class helpFlow(Flow):
    @start()
    def fetch_user_info(self):
        with open('user_persona.txt', 'r') as f:
            user_persona = f.read()
        
        with open('user_messages.txt', 'r') as f:
            question = f.read()

        print("A pergunta está clara? Se não, por favor, me diga o que está confuso.")
        user_feedback = input().strip()
        
        user_input = {
            'user_feedback': user_feedback,
            'user_persona': user_persona,
            'question': question
        }

        self.state.update(user_input)


        return user_input
    
    @listen(fetch_user_info)
    def guidance(self, user_input):
        help_message = help_crew.kickoff(inputs=user_input)
    
        with open('user_messages.txt', 'w+') as f:
            f.write(str(help_message))
        
        return help_message