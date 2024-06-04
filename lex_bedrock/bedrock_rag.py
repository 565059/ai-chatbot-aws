"""Módulo que interactúa con los servicios de Bedrock utilizando RAG"""

import logging

from langchain.chains.combine_documents.stuff import create_stuff_documents_chain
from langchain.chains.history_aware_retriever import create_history_aware_retriever
from langchain.chains.retrieval import create_retrieval_chain
from langchain.prompts import ChatPromptTemplate
from langchain_core.messages.ai import AIMessage
from langchain_core.messages.human import HumanMessage
from langchain_core.prompts import MessagesPlaceholder


class RAGRetriever:
    """"""

    def __init__(self, llm, retriever):
        self.llm = llm
        self.retriever = retriever

    def create_retriever_with_chat_history(self):
        """Crea un retriever con historial de chat"""

        contextualize_question_system_prompt = """
        Dado un historial de chat y la última pregunta del usuario,
        la cual puede que haga referencia al contexto en el historial de chat,
        formula una única pregunta que pueda ser entendida sin el historial
        de chat. NUNCA respondas a la pregunta, simplemente reformula la
        pregunta si es necesario y si no lo es, devuélvela como está.
        """
        contextualize_question_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", contextualize_question_system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        history_aware_retriever = create_history_aware_retriever(
            llm=self.llm,
            retriever=self.retriever,
            prompt=contextualize_question_prompt,
        )

        if history_aware_retriever is None:
            raise ValueError("Retriever is None")
        else:
            return history_aware_retriever

    def create_rag_chain(self):
        """Crea una cadena de RAG"""

        system_prompt = """
        Eres un asistente centrado en realizar tareas de preguntas y respuestas.
        Usa las siguientes partes del contexto recogido para contestar a la pregunta.
        Si no sabes la respuesta, dí que no lo sabes. Utiliza una frase como máximo
        y mantén la respuesta corta.
        \n\n
        {context}
        """

        qa_prompt = ChatPromptTemplate.from_messages(
            [
                ("system", system_prompt),
                MessagesPlaceholder("chat_history"),
                ("human", "{input}"),
            ]
        )

        qa_chain = create_stuff_documents_chain(
            llm=self.llm,
            prompt=qa_prompt,
        )

        rag_chain = create_retrieval_chain(
            retriever=self.create_retriever_with_chat_history(),
            combine_docs_chain=qa_chain,
        )

        if rag_chain is None:
            raise ValueError("RAG chain is None")
        else:
            return rag_chain

    def invoke(self, input_variables: dict):
        """Crea la respuesta a la pregunta del usuario y actualiza el historial de chat"""

        input_msg = input_variables["input"]
        chat_history = input_variables["chat_history"]

        complete_answer = ""
        try:
            rag_chain = self.create_rag_chain()
            complete_answer = rag_chain.invoke(
                {"input": input_msg, "chat_history": chat_history}
            )
        except ValueError as e:
            logging.error(e)
            answer = "Lo siento, pero parece que ha habido un problema."

        answer = complete_answer["answer"]
        chat_history.extend(
            [HumanMessage(content=input_msg), AIMessage(content=answer)]
        )

        return answer, chat_history
