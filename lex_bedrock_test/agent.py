from langgraph.prebuilt import create_react_agent
import config
from tools import Tools
from langchain.tools import Tool


class Agent():
    
    def __init__(self, llm, tools):
        self.ai_prefix = "Asistente"
        self.human_prefix = "Humano"
        self.llm = llm
        self.tools = tools
        
    def create_agent(self):
        pass