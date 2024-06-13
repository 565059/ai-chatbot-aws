import logging

import wikipediaapi
from langchain.agents.tools import Tool
from langchain.tools.retriever import create_retriever_tool
from langchain_aws import  AmazonKnowledgeBasesRetriever

tools_logger = logging.getLogger("TOOLS")
tools_logger.setLevel(logging.INFO)

class Tools:
    """Class containing tools used by the AI agent."""
    
    def __init__(self, env_config) -> None:
        """
        Initializes the Tools instance with tools created using environment configuration.

        Args:
        - env_config: Object holding environment configuration parameters.
        """
        self.tool_list = [
            self.create_kb_retriever_tool(env_config), 
            self.create_wikipedia_tool()
        ]
        
    def create_kb_retriever_tool(self, env_config):
        """
        Creates a tool using a knowledge base hosted on AWS.

        Args:
        - env_config: Object holding environment configuration parameters.

        Returns:
        - retriever_tool: Tool instance for knowledge base retrieval.
        """
        kb_retriever = AmazonKnowledgeBasesRetriever(
            knowledge_base_id=env_config.KNOWLEDGE_BASE_ID,
            retrieval_config={"vectorSearchConfiguration": {"numberOfResults": env_config.RESULTS_NUMBER}},
        )
        
        retriever_tool = create_retriever_tool(
            name="Knowledge Base",
            description="This tool provides access to a personalized knowledge base",
            retriever=kb_retriever
        )
        
        if retriever_tool:
            tools_logger.info("TOOLS: Knowledge Base tool created")
            return retriever_tool
        else:
            tools_logger.error("TOOLS: Error creating Knowledge Base tool")
    
    def search_wikipedia(self, title):
        """
        Searches Wikipedia to check if a page with the provided title exists.

        Args:
        - title: Title of the Wikipedia page to search for.

        Returns:
        - summary: Summary of the Wikipedia page if found, otherwise an error message.
        """
        wiki_wiki = wikipediaapi.Wikipedia('SampleProject/0.0 (example@example.com)', 'en')
        page = wiki_wiki.page(title)
        
        if page.exists():
            tools_logger.info(f"TOOLS: Page found on Wikipedia:\n{page.summary}")
            return page.summary 
        else:
            tools_logger.info("TOOLS: Page not found on Wikipedia")
            return "No exact page was found on Wikipedia matching the search."
        
    def create_wikipedia_tool(self):
        """
        Creates a tool for searching Wikipedia using a defined method and the 'wikipedia' library.

        Returns:
        - wikipedia_tool: Tool instance for Wikipedia search.
        """
        wikipedia_tool = Tool.from_function(
            func=self.search_wikipedia,
            name="Wikipedia",
            description="This tool provides access to Wikipedia to summarize or explain various topics you may not know by default."
        )
        
        if wikipedia_tool:
            tools_logger.info("TOOLS: Wikipedia tool created")
            return wikipedia_tool
        else:
            tools_logger.error("TOOLS: Error creating Wikipedia tool")
    
    
