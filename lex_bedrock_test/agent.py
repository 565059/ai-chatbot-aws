from langchain.agents import create_react_agent
from langchain.agents.agent import AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.messages import AIMessage, HumanMessage

from tools import Tools
import env_config


class ReactAgent:
    
    def __init__(self, llm, template, tools, session_id, chat_history):
        self.llm = llm
        self.template = template
        self.tools = tools
        self.session_id = session_id # event["session_id"]
        self.chat_history = chat_history
        
    def create_agent(self):
        prompt = PromptTemplate.from_template(self.template)
        
        
        memory = ChatMessageHistory(session_id=self.session_id, messages=self.chat_history)

        tools = Tools(env_config).tool_list
        
        react_agent = create_react_agent(
            llm=self.llm,
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
            return agent_with_history
        else:
            raise Exception("Error creating agent")

    def invoke(self, input_variables: dict): 
        """Crea la respuesta a la pregunta del usuario y actualiza el historial de chat"""

        input= input_variables["input"]
        chat_history = input_variables["chat_history"]

        complete_answer = ""
        
        config = {"configurable": {"session_id": self.session_id}}
        
        try:
            react_agent = self.create_agent()
            complete_answer = react_agent.invoke(
                {
                    "input": input, 
                    "chat_history": chat_history
                },
                config
            )
        except ValueError as e:
            print(e)
            answer = "Ha habido un problema invocando al agente."

        answer = complete_answer["output"]
        chat_history.extend(
            [HumanMessage(content=input), AIMessage(content=answer)]
        )

        return answer, chat_history
    