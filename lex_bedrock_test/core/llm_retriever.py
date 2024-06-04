import config.config as config
from langchain_aws import AmazonKnowledgeBasesRetriever, BedrockLLM

class LLM:
    def __init__(self, client, model_id, model_kwargs: dict):
        self.llm = BedrockLLM(
            client=client,
            model_id=model_id,
            model_kwargs=model_kwargs,
        )
        
        return self.llm
        
    def generate_response(self, query):
        return self.llm.invoke(query)
    
    
class KBRetriever:
    def __init__(self, knowledge_base_id, results_number):
        self.kb_retriever = AmazonKnowledgeBasesRetriever(
            knowledge_base_id=knowledge_base_id,
            retrieval_config={"vectorSearchConfiguration": {"numberOfResults": results_number}},
        )
        
    def retrieve_knowledge(self, query):
        return self.kb_retriever.retrieve(query)