import json
import logging

import env_config
from agent import ReactAgent
from langchain_aws import ChatBedrock
from messages import MessagesDecoder, MessagesEncoder
from tools import Tools


app_logger = logging.getLogger("APP")
app_logger.setLevel(logging.INFO)

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

tools = Tools(env_config).tool_list

# Template for the agent's prompt, guiding how it should respond to user queries
template = """You are an AI assistant responding to user questions in the language in which the question is written. The tools you might need to help you are:

[{tools}]

You don't have to use the tools to answer the user's question; use them only if you can't respond by yourself. Use the chat history enclosed within <chat_history> XML tags to help you contextualize the user's questions. To respond in the most concise and accurate way, you should use this format:

<chat_history>
[HumanMessage(content="Hello, my name is Pepe")], [AIMessage(content="Hello Pepe, I am an Artificial Intelligence")]
</chat_history>

Question: the question asked by the user that you need to answer; if you don't know the answer, say "Sorry, I don't know the answer to your question."
Thought: this is my notepad where I note down the steps I need to take to answer the question. I also ask myself: Do I need to use a tool? Yes
Action: the action you need to perform, it must be one of: [{tool_names}]
Action Input: the input you must provide to the tool; NEVER return the tool's result in this step
Observation: the result of the action; if it returns nothing, say "I don't know."
... (this Thought/Action/Action Input/Observation format CANNOT BE REPEATED)

If you don't need to use a tool to answer the question or have achieved the result from performing the action, you MUST use this format:

Thought: Do I need to use a tool? No
Action: retrieve the answer
Final Answer: the final answer to the user's original question is: [final answer]


Let's begin!

{chat_history}

Question: {input}
Thought: {agent_scratchpad}"""


def lex_format_response(event, response_text, chat_history, content_type):
    """
    Creates the response format required by Lex, including chat history
    and the type of response: SSML (Audio) | PlainText (Text)

    Args:
        event: The event data from Lex.
        response_text: The response text to be sent to the user.
        chat_history: The updated chat history.
        content_type: The type of content, either "SSML" or "PlainText".

    Returns:
        A dictionary representing the formatted response.
    """
    event["sessionState"]["intent"]["state"] = "Fulfilled"

    if content_type == "SSML":
        app_logger.info("APP: SSML response")
        return {
            "sessionState": {
                "sessionAttributes": {"chat_history": chat_history},
                "dialogAction": {"type": "Close"},
                "intent": event["sessionState"]["intent"],
            },
            "messages": [
                {
                    "contentType": "SSML",
                    "content": f"""
                        <speak>
                            <lang xml:lang="es-ES">
                                {response_text}
                            </lang>
                        </speak>
                    """,
                }
            ],
            "sessionId": event["sessionId"],
            "requestAttributes": (
                event["requestAttributes"] if "requestAttributes" in event else None
            ),
        }

    else:
        app_logger.info("APP: PlainText response")
        return {
            "sessionState": {
                "sessionAttributes": {"chat_history": chat_history},
                "dialogAction": {"type": "Close"},
                "intent": event["sessionState"]["intent"],
            },
            "messages": [
                {
                    "contentType": "PlainText",
                    "content": response_text,
                },
            ],
            "sessionId": event["sessionId"],
            "requestAttributes": (
                event["requestAttributes"] if "requestAttributes" in event else None
            ),
        }


def load_chat_history(session):
    """
    Transforms the JSON retrieved from the session into messages of type 
    AIMessage or HumanMessage.

    Args:
        session: The session data containing chat history.

    Returns:
        A list of messages decoded from JSON.
    """
    if "chat_history" in session:
        return json.loads(session["chat_history"], cls=MessagesDecoder)
    else:
        return []
    
def save_chat_history(chat_history):
    """
    Transforms the list of messages of type AIMessage or HumanMessage 
    into a JSON string. If there are more than 6 messages in the chat history,
    it removes the first 3 messages.

    Args:
        chat_history: The current chat history as a list of messages.

    Returns:
        A JSON string representing the updated chat history.
    """
    if len(chat_history) > 6:
        chat_history = chat_history[-3:]
    return json.dumps(chat_history, cls=MessagesEncoder)

def lambda_handler(event, context):
    """
    Lambda function to handle the input event and context from Lex.

    Args:
        event: The event data from Lex.
        context: The context data for the Lambda execution.

    Returns:
        The formatted response to be sent to Lex.
    """
    if event["inputTranscript"]:
        user_input = event["inputTranscript"]
        session = event["sessionState"]["sessionAttributes"]
        input_mode = event["inputMode"]
        session_id = event["sessionId"]

        content_type = "SSML" if input_mode == "Speech" else "PlainText"
        
        chat_history = load_chat_history(session)
        
        agent = ReactAgent(llm, template, tools, session_id, chat_history)

        if user_input.strip() == "":
            result = {"answer": "Por favor, realiza una pregunta."}
        else:
            input_variables = {"input": user_input, "chat_history": chat_history}

            result = agent.invoke(input_variables)

            answer, chat_history = result
            
        chat_history = save_chat_history(chat_history)

        return lex_format_response(
            event,
            answer,
            chat_history,
            content_type,
        )
