import json
import logging
import os

import boto3
from bedrock_rag import BedrockRAG
from messages import MessagesDecoder, MessagesEncoder
from langchain_aws import AmazonKnowledgeBasesRetriever, BedrockLLM
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage

region_name = os.environ["AWS_REGION"]
model_id = os.environ["MODEL_ID"]
knowledgebase_id = os.environ["KNOWLEDGE_BASE_ID"]
temperature = float(os.environ["TEMPERATURE"])
top_k = int(os.environ["TOP_K"])
max_tokens = int(os.environ["MAX_TOKENS"])
results_number = int(os.environ["RESULTS_NUMBER"])

boto3_session = boto3.Session(region_name=region_name)
bedrock_client = boto3_session.client("bedrock")
bedrock_runtime_client = boto3_session.client("bedrock-runtime")

bedrock_llm = BedrockLLM(
    client=bedrock_runtime_client,
    model_id=model_id,
    model_kwargs={
        "temperature": temperature,
        "top_k": top_k,
        "max_tokens_to_sample": max_tokens,
    },
)

kb_retriever = AmazonKnowledgeBasesRetriever(
    knowledge_base_id=knowledgebase_id,
    retrieval_config={"vectorSearchConfiguration": {"numberOfResults": results_number}},
)

bedrock_rag = BedrockRAG(
    llm=bedrock_llm,
    retriever=kb_retriever,
)


def lex_format_response(event, response_text, chat_history, content_type):
    """Formatea la respuesta del bot al formato de evento de Lex"""

    event["sessionState"]["intent"]["state"] = "Fulfilled"

    if content_type == "SSML":
        return {
            "sessionState": {
                "sessionAttributes": {"chat_history": chat_history},
                "dialogAction": {"type": "Close"},
                "intent": event["sessionState"]["intent"],
            },
            "messages": [
                {
                    "contentType": "SSML",
                    "content": f"<speak>{response_text}</speak>",
                }
            ],
            "sessionId": event["sessionId"],
            "requestAttributes": (
                event["requestAttributes"] if "requestAttributes" in event else None
            ),
        }

    else:
        return {
            "sessionState": {
                "sessionAttributes": {"chat_history": chat_history},
                "dialogAction": {"type": "Close"},
                "intent": event["sessionState"]["intent"],
            },
            "messages": [
                {
                    "contentTyoe": "PlainText",
                    "content": response_text,
                },
            ],
            "sessionId": event["sessionId"],
            "requestAttributes": (
                event["requestAttributes"] if "requestAttributes" in event else None
            ),
        }


def lambda_handler(event, context):
    """Función principal de la lambda"""

    if event["inputTranscript"]:
        user_input = event["inputTranscript"]
        session = event["sessionState"]["sessionAttributes"]
        input_mode = event["inputMode"]

        content_type = "SSML" if input_mode == "Speech" else "PlainText"

        # Cargar el historial de chat de la lambda anterior
        if "chat_history" in session:
            chat_history = json.loads(session["chat_history"], cls=MessagesDecoder)
        else:
            chat_history = []

        if user_input.strip() == "":
            result = {"answer": "Por favor, realiza una pregunta."}
        else:
            input_variables = {"input": user_input, "chat_history": chat_history}

            logging.info("Input variables: %s", input_variables)

            result = bedrock_rag.invoke(input_variables)

            answer, chat_history = result

        if answer:
            response_text = answer.strip()
        else:
            response_text = "No lo sé."

        chat_history.append(HumanMessage(content=user_input))
        chat_history.append(AIMessage(content=response_text))
        if len(chat_history) > 6:
            chat_history = chat_history[-3:]

        return lex_format_response(
            event,
            response_text,
            json.dumps(chat_history, cls=MessagesEncoder),
            content_type,
        )
