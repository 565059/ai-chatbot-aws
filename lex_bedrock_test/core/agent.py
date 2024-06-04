from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.base import 
from llm_retriever import LLM
import config.config as config


class Agent():
    
    def __init__(self, llm, tools):
        self.agent_executor = create_react_agent(
            model=llm,
            tools=tools
        )