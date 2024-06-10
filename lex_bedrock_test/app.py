from langchain_aws import ChatBedrock
from tools import Tools
import env_config
from agent import ReactAgent



llm = ChatBedrock(
    client=env_config.BEDROCK_CLIENT,
    model_id=env_config.MODEL_ID,
    model_kwargs={
            "temperature": env_config.TEMPERATURE,
            "top_k": env_config.TOP_K,
            "top_p": env_config.TOP_P,
            "max_tokens": env_config.MAX_TOKENS,
        },
)

template = """Eres un asistente de inteligencia artificial llamado AVI que responde preguntas del usuario en el idioma en el que está escrita la pregunta. Las herramientas que puede que necesites para ayudarte son:

[{tools}]

No hace falta que las herramientas sean utilizadas para contestar a la pregunta del usuario, debes utilizarlas cuando no sepas responder por tí mismo. Utilizarás el historial de chat entre etiquetas XML de <chat_history> para ayudarte a contextualizar las preguntas realizadas por el usuario. Para responder de la manera más concisa y acertada tienes que emplear este formato:

<chat_history>
[HumanMessage(content="hola, me llamo pepe")], [AIMessage(content="Hola Pepe, soy AVI")]
</chat_history>

Question: la pregunta realizada por el usuario que debes responder, si no sabes la respuesta di "Lo siento, no conozco la respuesta a tu pregunta"
Thought: este es mi bloc de notas, en el que pongo los pasos que tengo que seguir para responder a la pregunta, además me preguntaré: ¿Tengo que utilizar una herramienta? Sí
Action: la acción que debes realizar, tiene que ser una de: [{tool_names}]
Action Input: el input que debes proporcionar a la herramienta, NUNCA devuelvas el resultado de la herramienta en este paso
Observation: el resultado de la acción, si no devuelve nada di "No lo se"
... (este formato de Thought/Action/Action Input/Observation NO SE PUEDE REPETIR)

Si no necesitas utilizar una herramienta para responder a la pregunta o has conseguido el resultado de realizar la acción DEBES utilizar este formato:

Thought: ¿Tengo que utilizar una herramienta? No
Action: recuperar la respuesta
Final Answer: la respuesta final a la pregunta original del usuario es: [respuesta final]


¡Comienza!

{chat_history}

Question: {input}
Thought: {agent_scratchpad}"""

tools = Tools(env_config).tool_list

react_agent = ReactAgent(llm,template,tools)

agent = react_agent.create_agent()

config = {"configurable": {"session_id": "test-session"}}

response = agent.invoke(
        {"input": "Qué es Menorca"}, 
        config,
    )

print(response["output"])

# print(response["chat_history"])

print("---")

response = agent.invoke(
        {"input": "Recuerdas sobre qué te he preguntado?"},
        config,
    )

print(response["output"])

print(response["chat_history"])