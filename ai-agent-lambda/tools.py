from langchain.agents.tools import Tool
from langchain.tools.retriever import create_retriever_tool
from langchain_aws import  AmazonKnowledgeBasesRetriever
import wikipedia
import wikipediaapi

class Tools:
    """Clase que contiene las herramientas utilizadas por el agente de IA."""
    
    def __init__(self, env_config) -> None:
        self.tool_list = [self.create_kb_retriever_tool(env_config), self.create_wikipedia_tool()]
        
        
    def create_kb_retriever_tool(self, env_config):
        """Método que crea una herramienta a partir de una base de conocimiento alojada en AWS."""
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
    
    def search_wikipedia(self, title):
        """Método que busca en Wikipedia para saber si la página con el título proporcionado existe."""
        wiki = wikipediaapi.Wikipedia('es')
        page = wiki.page(title)
        
        if page.exists():
            return page.title
        else:
            return None
        
    def get_wikipedia_page_summary(self, query):
        """Método que crea un resumen de la página encontrada por el método 'search_wikipedia'."""
        title = self.search_wikipedia(query)
        if title:
            return wikipedia.summary(title)
        else:
            return "No se encontró ninguna página exacta en Wikipedia que coincida con la búsqueda."
        
    def create_wikipedia_tool(self):
        """Método que crea una herramienta de búsqueda en Wikipedia a partir de un método y la biblioteca de 'wikipedia'."""
        wikipedia_tool = Tool.from_function(
            func=self.get_wikipedia_page_summary,
            name="Wikipedia",
            description="Con esta herramienta podrás acceder a Wikipedia para resumir o explicar temas variados que no conozcas por defecto y que no tengan relación con Enclave Formación."
        )
        
        if wikipedia_tool:
            return wikipedia_tool
        else:
            raise Exception("Error al crear la herramienta de Wikipedia")
    
    