from lex_bedrock_test import config
from langchain_aws import  AmazonKnowledgeBasesRetriever, ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langgraph.prebuilt import create_react_agent
from langchain.tools.retriever import create_retriever_tool


# METERLE PROMPTS PERSONALIZADOS PARA QUE NO ALUCINE PEPINILLOS
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
        description="Utiliza esta herramienta para responder preguntas y proporcionar información sobre cursos de formación de forma concisa y precisa. Si no encuentras la información en la base de conocimientos di que no lo sabes.",
        retriever=kb_retriever
    )

query = "¿Qué productos oferta Enclave Formación?"
messages = [
    SystemMessage(content="Eres un asistente llamado AVI, eres propiedad de la empresa Enclave Formación S.L, ayudas a los humanos que te preguntan utilizando las herramientas que se te han proporcionado."),
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
