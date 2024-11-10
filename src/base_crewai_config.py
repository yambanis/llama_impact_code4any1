# Warning control
import warnings
warnings.filterwarnings('ignore')

import os
import yaml
from crewai import LLM

llm = LLM(
    model="groq/llama-3.1-70b-versatile", 
    #model="groq/llama-3.1-8b-instant",
    api_key=os.getenv("GROQ_API_KEY")
)
# Define file paths for YAML configurations
files = {
    'agents': 'configs/agents.yaml',
    'tasks': 'configs/tasks.yaml'
}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']