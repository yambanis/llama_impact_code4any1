from llama_impact_code4any1.crews.onboarding import onboardingFlow
from llama_impact_code4any1.crews.questions import questionFlow
from llama_impact_code4any1.crews.help import helpFlow

oflow = onboardingFlow()
oflow.kickoff()

print("**Finished onboarding flow**")

qflow = questionFlow()
question = qflow.kickoff()

print("**Finished Question Flow**")
print(question)

hflow = helpFlow()
help_message = hflow.kickoff()

print("**Finished Help Flow**")
print(help_message)