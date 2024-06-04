from langchain.agents.tools import Tool


class Tools:
    
    def __init__(self) -> None:
        self.tools = [
            Tool(
                name="RetrieveCourses",
                func=self.search_kb,
                description="Utiliza esta herramienta para responder preguntas sobre los cursos de formación de Enclave Formación S.L."
            )
        ]
        
    def search_kb(self, query):
        pass