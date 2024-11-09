from crewai import Agent


def create_agent(llm, config):
    agent = Agent(
        config=config,
        llm=llm,
        human_input=False
    )

    return agent
