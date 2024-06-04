from lex_bedrock_test import config
from langchain_aws import  AmazonKnowledgeBasesRetriever, ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langchain.tools.retriever import create_retriever_tool



llm = ChatBedrock(
    client=config.BEDROCK_CLIENT,
    model_id=config.MODEL_ID,
    model_kwargs={
            "temperature": config.TEMPERATURE,
            "top_k": config.TOP_K,
        },
)

kb_retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id=config.KNOWLEDGE_BASE_ID,
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": config.RESULTS_NUMBER}},
)

retriever_tool = create_retriever_tool(
        name="knowledge_base_retriever",
        description="Utiliza esta herramienta para responder preguntas sobre los cursos de formación de Enclave Formación S.L.",
        retriever=kb_retriever
    )

query = "¿Cuánto dura el curso de fotografía?"
messages = [
    SystemMessage(content="Eres un asistente que ayuda al humano utilizando las herramientas proporcionadas."),
    HumanMessage(content=query)
]

tools = [retriever_tool]

agent_executor = create_react_agent(
    model=llm,
    tools=tools,
)

for s in agent_executor.stream(
    {"messages": messages}
):
    print(s)
    print("----")
