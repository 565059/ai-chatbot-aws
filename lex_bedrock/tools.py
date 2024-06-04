from langchain.tools.retriever import create_retriever_tool
from bedrock_rag import RAGRetriever
from langchain.tools import BaseTool
from langgraph.prebuilt import create_react_agent


def test(llm, retriever):
    kb_retriever_tool = create_retriever_tool(
        retriever=RAGRetriever(retriever=retriever, llm=llm).create_retriever_with_chat_history(),
        name="knowledge_base_retriever",
        description="Retrieve information from the knowledge base."
    )
    
    return kb_retriever_tool

agent_executor = create_react_agent(
    llm=llm
    tools=[
        test,
    ]
)

