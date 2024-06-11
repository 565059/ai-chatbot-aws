from langchain.agents.tools import Tool
from langchain.tools.retriever import create_retriever_tool
from langchain_aws import  AmazonKnowledgeBasesRetriever
import wikipedia

class Tools:
    
    def __init__(self, env_config) -> None:
        self.tool_list = [self.create_kb_retriever_tool(env_config), self.create_wikipedia_tool()]
        
        
    def create_kb_retriever_tool(self, env_config):
        kb_retriever = AmazonKnowledgeBasesRetriever(
            knowledge_base_id=env_config.KNOWLEDGE_BASE_ID,
            retrieval_config={"vectorSearchConfiguration": {"numberOfResults": env_config.RESULTS_NUMBER}},
        )
        
        retriever_tool = create_retriever_tool(
            name="Base de conocimiento de Enclave Formación",
            description="Con esta herramienta podrás acceder a una base de conocimiento sobre Enclave Formación y sus cursos de formación.",
            retriever=kb_retriever
        )
        
        if retriever_tool:
            return retriever_tool
        else:
            raise Exception("Error al crear la herramienta de base de conocimiento")
        
        
    def create_wikipedia_tool(self):
        wikipedia_tool = Tool.from_function(
            func=wikipedia.summary,
            name="Wikipedia",
            description="Con esta herramienta podrás crear resúmenes acerca de temas de actualidad."
        )
        
        if wikipedia_tool:
            return wikipedia_tool
        else:
            raise Exception("Error al crear la herramienta de Wikipedia")
    
