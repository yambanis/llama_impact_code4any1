from llama_impact_code4any1.crews.onboarding import onboardingFlow
from llama_impact_code4any1.crews.questions import questionFlow
from llama_impact_code4any1.crews.help import helpFlow
from llama_impact_code4any1.crews.curriculum import curriculumFlow

oflow = onboardingFlow()
oflow.plot("onboarding_flow")
oflow.kickoff()
print("**Finished onboarding flow**")

cflow = curriculumFlow()
cflow.plot("curriculum_flow")
curriculum = cflow.kickoff()
print("**Finished Curriculum Flow**")

qflow = questionFlow()
qflow.plot("question_flow")
question = qflow.kickoff()

print("**Finished Question Flow**")
print(question)

hflow = helpFlow()
hflow.plot("help_flow")
help_message = hflow.kickoff()

print("**Finished Help Flow**")
print(help_message)