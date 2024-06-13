import logging

from langchain.agents import create_react_agent, AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage, HumanMessage


agent_logger = logging.getLogger("AGENT")
agent_logger.setLevel(logging.INFO)

class ReactAgent:
    """
    Class to create a ReAct agent with memory using tools like Wikipedia 
    and a knowledge base.
    """
    def __init__(self, llm, template, tools, session_id, chat_history):
        """
        Initializes the ReactAgent instance.

        Args:
            llm: The language model to use.
            template: The prompt template to use.
            tools: The tools for the agent.
            session_id: The unique session identifier.
            chat_history: The previous chat history.
        """
        self.session_id = session_id
        self.react_agent = self.create_memory_react_agent(llm, template, tools, session_id, chat_history)
        
    def create_memory_react_agent(self, llm, template, tools, session_id, chat_history):
        """
        Creates a ReAct agent with memory.

        Args:
            llm: The language model to use.
            template: The prompt template to use.
            tools: The tools for the agent.
            session_id: Unique session identifier.
            chat_history: Previous chat history.

        Returns:
            An instance of RunnableWithMessageHistory if successful, otherwise logs an error.
        """
        prompt = PromptTemplate.from_template(template)
        
        memory = ChatMessageHistory(session_id=session_id, messages=chat_history)
        
        react_agent = create_react_agent(
            llm=llm,
            tools=tools,
            prompt=prompt,
        )
        
        agent_executor = AgentExecutor(
            agent=react_agent, 
            tools=tools,
            # verbose=True,
            handle_parsing_errors=True
        )
        
        agent_with_history = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: memory,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        
        if agent_with_history:
            agent_logger.info("AGENT: Agente creado con éxito")
            return agent_with_history
        else:
            agent_logger.error("AGENT: Error al crear el agente")

    def invoke(self, input_variables: dict): 
        """
        Generates a response to the user's query and updates the chat history.

        Args:
            input_variables: Dictionary containing the user input and chat history.

        Returns:
            A tuple with the agent's response and the updated chat history.
        """

        input= input_variables["input"]
        chat_history = input_variables["chat_history"]

        complete_answer = ""
        
        config = {"configurable": {"session_id": self.session_id}}
        
        try:
            complete_answer = self.react_agent.invoke(
                {
                    "input": input, 
                    "chat_history": chat_history
                },
                config
            )
        except ValueError as e:
            agent_logger.error(f"AGENT: Ha habido un problema invocando el agente:\n{e}")

        answer = complete_answer["output"]
        chat_history.extend(
            [HumanMessage(content=input), AIMessage(content=answer)]
        )

        agent_logger.info(f"AGENT: Respuesta del agente: \n{answer}")
        return answer, chat_history
    
