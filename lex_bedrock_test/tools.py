from langchain.agents.tools import Tool
from langchain.tools.retriever import create_retriever_tool

class Tools:
     
    def __init__(self, kb_history_aware_retriever) -> None:
        self.retriever_tool = create_retriever_tool(
            name="knowledge_base_retriever",
            description="Utiliza esta herramienta para responder preguntas sobre los cursos de formación de Enclave Formación S.L.",
            retriever=kb_history_aware_retriever
        )