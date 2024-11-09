from crewai import Flow, Crew
from crewai.flow.flow import start, listen
from src.agents import create_agent
from src.tasks import create_task


class FullFlow(Flow):
    def __init__(self, llm, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.agents_config = config['agents']
        self.tasks_config = config['tasks']
        self.onboarding_agent = create_agent(llm, self.agents_config['onboarding_agent'])
        self.question_agent = create_agent(llm, self.agents_config['question_creation_agent'])

        self.user_onboarding_task = create_task(self.tasks_config['user_onboarding'], self.onboarding_agent, [])
        self.question_creation_task = create_task(self.tasks_config['question_creation'], self.question_agent, [self.user_onboarding_task])
        self.question_critic_task = create_task(self.tasks_config['question_critic'], self.question_agent, [self.user_onboarding_task, self.question_creation_task])

        self.onboarding_crew = Crew(
            agents=[
                self.onboarding_agent
            ],
            tasks=[
                self.user_onboarding_task
            ],
            verbose=False
        )

        self.question_crew = Crew(
            agents=[
                self.question_agent
            ],
            tasks=[
                self.question_creation_task,
                self.question_critic_task
            ],
            verbose=False
        )

    @start()
    def fetch_user(self):
        user_input =  {
            'user_input': self._state['message']
        }    
        return user_input
    
    @listen(fetch_user)
    def onboarding(self, user_input):
        user_info = self.onboarding_crew.kickoff(inputs=user_input)
        self.state['user_info'] = user_info

        return user_info
    
    @listen(onboarding)
    def question_creation(self, user_info):
        question = self.question_crew.kickoff()
        print(question)
    
        return question
