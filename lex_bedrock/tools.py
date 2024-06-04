from langchain.tools.retriever import create_retriever_tool
import bedrock_rag


retriever_tool = create_retriever_tool(
    retriever=bedrock_rag.
)