from lex_bedrock_test import config
from langchain_aws import  AmazonKnowledgeBasesRetriever, ChatBedrock
from langchain_core.messages import HumanMessage, SystemMessage, AIMessage
from langchain.agents import create_react_agent
from langchain.agents.agent import AgentExecutor
from langchain.tools.retriever import create_retriever_tool
from langchain_core.prompts import PromptTemplate
from langchain.chains.llm_math.base import LLMMathChain
from langchain.tools import Tool

import logging
import streamlit as st

llm = ChatBedrock(
    client=config.BEDROCK_CLIENT,
    model_id=config.MODEL_ID,
    model_kwargs={
            "temperature": config.TEMPERATURE,
            "top_k": config.TOP_K,
            "top_p": config.TOP_P,
            "max_tokens": config.MAX_TOKENS,
        },
)

llm_math_chain = LLMMathChain.from_llm(
    llm=llm,
)

calc_tool = Tool.from_function(
    func=llm_math_chain.invoke,
    name="Calculadora",
    description="Utiliza esta herramienta cuando necesites responder preguntas sobre matemáticas."
)

kb_retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id=config.KNOWLEDGE_BASE_ID,
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": 4}},
)

retriever_tool = create_retriever_tool(
    name="Base de conocimiento",
    description="Con esta herramienta podrás acceder a una base de conocimiento sobre cursos de formación.",
    retriever=kb_retriever
)

template = """Eres un agente de inteligencia artificial llamado AVI que responde preguntas del usuario en el idioma en el que está escrita la pregunta. Las herramientas que puede que necesites para ayudarte son:

{tools}

No hace falta que las herramientas sean utilizadas para contestar a la pregunta del usuario, debes utilizarlas cuando no sepas responder por tí mismo. Para responder de la manera más concisa y acertada tienes que emplear este formato:

Question: la pregunta realizada por el usuario que debes responder, si no sabes la respuesta di "Lo siento, no conozco la respuesta a tu pregunta"
Thought: este es mi bloc de notas, en el que pongo los pasos que tengo que seguir para responder a la pregunta, además me preguntaré: ¿Tengo que utilizar una herramienta? Sí
Action: la acción que debes realizar, tiene que ser una de: [{tool_names}]
Action Input: el input que se le tiene que pasar a la herramienta
Observation: el resultado de la acción, si no devuelve nada di "No lo se"
... (este formato de Thought/Action/Action Input/Observation NO SE PUEDE REPETIR)

Si no necesitas utilizar una herramienta para responder a la pregunta o tienes el resultado de realizar la acción DEBES utilizar este formato:

Thought: ¿Tengo que utilizar una herramienta? No
Action: recuperar la respuesta
Final Answer: la respuesta final a la pregunta original del usuario es: [respuesta final]


¡Comienza!

Question: {input}
Thought: {agent_scratchpad}"""

prompt = PromptTemplate.from_template(template)

agent = create_react_agent(
        llm=llm,
        tools=[retriever_tool, calc_tool],
        prompt=prompt
    )

agent_executor = AgentExecutor.from_agent_and_tools(agent=agent, tools=[retriever_tool, calc_tool],verbose=True,handle_parsing_errors=True, return_intermediate_steps=True)

st.title("Chat with AI")

query = st.text_input("Habla con la IA:")
button = st.button("Enviar")

if button:
    messages = [
        SystemMessage(content="Eres un asistente llamado AVI, propiedad de la empresa Enclave Formación S.L, ayudas a los humanos que te preguntan utilizando las herramientas que se te han proporcionado."),
    ]
    

    st.write(agent_executor.invoke({"input": query,"messages": messages})["output"])


    
