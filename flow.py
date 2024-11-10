from src.crews.curriculum import curriculumFlow
from src.crews.help import helpFlow
from src.crews.onboarding import onboardingFlow
from src.crews.questions import questionFlow

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