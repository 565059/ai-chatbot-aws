from langchain.agents.tools import Tool
from langchain.tools.retriever import create_retriever_tool
from lex_bedrock_test import config
from langchain_aws import  AmazonKnowledgeBasesRetriever, ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.agents import create_react_agent
from langchain.agents.agent import AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm_math.base import LLMMathChain
from langchain.tools import Tool

class Tools:
     
    def __init__(self, config) -> None:
        self.kb_retriever_tool = self.create_kb_retriever_tool()
        
    def create_kb_retriever_tool(self):
        kb_retriever = AmazonKnowledgeBasesRetriever(
            knowledge_base_id=config.KNOWLEDGE_BASE_ID,
            retrieval_config={"vectorSearchConfiguration": {"numberOfResults": config.RESULTS_NUMBER}},
        )
        
        retriever_tool = create_retriever_tool(
            name="Base de conocimiento",
            description="Con esta herramienta podrás acceder a una base de conocimiento sobre cursos de formación.",
            retriever=kb_retriever
        )
        
        if retriever_tool:
            return retriever_tool
        else:
            raise Exception("Error al crear la herramienta de base de conocimiento")
        
    def create_tool(self):
        pass