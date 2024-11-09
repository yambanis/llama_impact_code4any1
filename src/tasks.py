from crewai import Task

def create_task(config, agent, context):
    return Task(
        config=config,
        agent=agent,
        context=context
    )