from crewai import Agent, Crew, Flow, Task
from crewai.flow.flow import listen, start

from llama_impact_code4any1.crews.base_config import agents_config, llm, tasks_config

# Creating Agents
onboarding_agent = Agent(
  config=agents_config['onboarding_agent'],
  llm=llm,
  human_input=True
)

# Creating Tasks
user_onboarding = Task(
  config=tasks_config['user_onboarding'],
  agent=onboarding_agent
)

onboarding_crew = Crew(
  agents=[
    onboarding_agent
  ],
  tasks=[
    user_onboarding
  ],
  verbose=False
)

class onboardingFlow(Flow):
    @start()
    def fetch_user(self):
        print("Me conte sobre você")
        user_input = {
            'user_input': input()
        }
        return user_input

    @listen(fetch_user)
    def onboarding(self, user_input):
        user_info = onboarding_crew.kickoff(inputs=user_input)
        with open('user_persona.txt', 'w') as f:
            f.write(str(user_info))

        return user_info