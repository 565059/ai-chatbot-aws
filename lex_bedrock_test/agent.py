from lex_bedrock_test.agent_tests import config

from langchain.agents import create_react_agent
from langchain.agents.agent import AgentExecutor
from langchain_core.prompts import PromptTemplate
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.runnables.history import RunnableWithMessageHistory

from tools import Tools

import json
import logging
import streamlit as st


class ReactAgent:
    
    def __init__(self, llm, template, tools):
        self.llm = llm
        self.template = template
        self.tools = tools
        #self.history = history
        self.react_agent = self.create_agent()
        
    def create_agent(self):
        prompt = PromptTemplate.from_template(self.template)
             
        chat_history = ChatMessageHistory(session_id="test-session")

        tools = Tools(config).tool_list
        
        react_agent = create_react_agent(
            llm=self.llm,
            tools=tools,
            prompt=prompt,
        )
        
        agent_executor = AgentExecutor(
            agent=react_agent, 
            tools=tools,
            verbose=True,
            handle_parsing_errors=True
        )
        
        agent_with_history = RunnableWithMessageHistory(
            agent_executor,
            lambda session_id: chat_history,
            input_messages_key="input",
            history_messages_key="chat_history",
        )
        
        if agent_with_history:
            return agent_with_history
        else:
            raise Exception("Error creating agent")


    