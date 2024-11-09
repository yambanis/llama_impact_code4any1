# Warning control
import warnings
warnings.filterwarnings('ignore')

import os
import yaml
from crewai import LLM

llm = LLM(
    model="groq/llama-3.1-70b-versatile", 
    #model="groq/llama-3.1-8b-instant",
    api_key="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"
)
# Define file paths for YAML configurations
files = {
    'agents': 'configs/basic_config/agents.yaml',
    'tasks': 'configs/basic_config/tasks.yaml'
}

# Load configurations from YAML files
configs = {}
for config_type, file_path in files.items():
    with open(file_path, 'r') as file:
        configs[config_type] = yaml.safe_load(file)

# Assign loaded configurations to specific variables
agents_config = configs['agents']
tasks_config = configs['tasks']