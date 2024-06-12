# 🤖 AI Chatbot with LangChain and AWS

_Social_

[![565059 - ai-chatbot](https://img.shields.io/badge/565059-000000?logo=github&logoColor=ffffff)](https://github.com/565059 "Go to 565059's GitHub")

_Services used_

[![Python - 3.12.0](https://img.shields.io/static/v1?label=Python&message=v3.12.0&color=3776AB&labelColor=3776AB&logo=python&logoColor=ffffff)](https://www.python.org/downloads/release/python-3120/ "Go to Python") [![LangChain](https://img.shields.io/badge/🦜️🔗Langchain-v0.2.3-1C3C3C?&labelColor=1C3C3C)](https://github.com/langchain-ai "Go to LangChain") [![Wikipedia-API](https://img.shields.io/badge/Wikipedia--API-v0.6.8-000000?logo=wikipedia&logoColor=ffffff&labelColor=000000)](https://github.com/martin-majlis/Wikipedia-API "Go to Wikipedia-API") [![AWS SDK - Boto3](https://img.shields.io/badge/Boto3-v1.34.124-232f3e?logo=amazonwebservices&logoColor=ffffff&labelColor=232f3e)](https://github.com/boto/boto3 "Go to Boto3") 

## 📋 Summary

This project develops an intelligent chatbot that generates automatic responses using generative artificial intelligence and a dynamic knowledge base. The solution integrates various Amazon Web Services (AWS) and leverages the LangChain libraries and the Wikipedia API to enrich responses.

## 🤔 Generative AI with RAG

A ReAct Agent AI type has been implemented, utilizing the Retrieval Augmented Generation (RAG) technique to provide accurate and up-to-date responses. This agent interacts with two key tools:

Knowledge Base: It employs RAG to retrieve relevant information on specific topics, such as company salary data.
Wikipedia: It uses the Wikipedia API to access a wide range of information, enriching the responses with accurate and varied data.

## ☁️ AWS Services Used

The solution relies on several AWS services to ensure smooth integration and cost efficiency. The main services are:

* 📁 S3: Stores .pdf files containing structured information that the chatbot uses to generate clear and precise responses.
* 💬 Lex: Provides the user interface for the chatbot, including voice services like Amazon Transcribe and Amazon Polly.
* 🧠 Bedrock: Acts as the hub for foundational model (FM) selection and hosts the knowledge base.
* ⚙ Lambda: Functions as a serverless service facilitating calls to the AI agent and its tools, offering automatic scalability, security, and flexibility.

## 📚 Libraries and Tools

🦜️🔗 LangChain: Enables the integration and orchestration of different AI tools and knowledge bases, facilitating the creation of a robust AI agent.
🌍 Wikipedia-API: Provides access to extensive and updated data from Wikipedia, enriching the chatbot's capabilities.

## 🚀 Functionality Description

The general flow of the chatbot is as follows:

1. Event Reception: AWS Lambda receives an event from Amazon Lex.
1. Response Generation: Lambda calls the AI agent that uses LangChain to process the event.
1. Knowledge Base Query: The agent employs RAG to search for information in the knowledge base hosted on Amazon Bedrock.
1. Access to Wikipedia: If additional information is needed, the agent queries Wikipedia using its API.
1. User Response: The generated response is formatted and sent back to Amazon Lex, which presents it to the user.

