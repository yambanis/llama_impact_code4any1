from crewai import Agent, Crew, Flow, Task
from crewai.flow.flow import listen, start
from crewai_tools import SerperDevTool
from src.crews.base_config import agents_config, llm, tasks_config

explanation_creation_agent = Agent(
    config=agents_config["explanation_creation_agent"], llm=llm
)

search_tool = SerperDevTool()

explain_topic = Task(
    config=tasks_config["explain_topic"],
    agent=explanation_creation_agent,
    tools=[search_tool],
)

choose_topic = Task(
    config=tasks_config["choose_topic"],
    agent=explanation_creation_agent,
    tools=[],
)

explain_crew = Crew(
    agents=[explanation_creation_agent], tasks=[explain_topic], verbose=False
)

topic_picking_crew = Crew(
    agents=[explanation_creation_agent], tasks=[choose_topic], verbose=False
)


class explanationFlow(Flow):
    @start()
    def fetch_user_info(self):
        with open("user_persona.txt", "r") as f:
            user_persona = f.read()

        with open("curriculum.txt", "r") as f:
            curriculum = f.read()

        user_input = {
            "curriculum": curriculum,
            "user_persona": user_persona,
        }

        self.state.update(user_input)

        return user_input

    @listen(fetch_user_info)
    def topic_chooser(self, user_input):
        topic = topic_picking_crew.kickoff(inputs=user_input)

        return {
            "user_persona": user_input["user_persona"],
            "topic": topic.raw,
        }

    @listen(topic_chooser)
    def topic_explainer(self, inputs):
        print("Entrou no topic explainer")
        explain_message = explain_crew.kickoff(inputs=inputs)

        return explain_message