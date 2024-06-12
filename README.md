📋 Summary

This project develops an intelligent chatbot that generates automatic responses using generative artificial intelligence and a dynamic knowledge base. The solution integrates various Amazon Web Services (AWS) and leverages the LangChain libraries and the Wikipedia API to enrich responses.

🤔 Generative AI with RAG

A ReAct Agent AI type has been implemented, utilizing the Retrieval Augmented Generation (RAG) technique to provide accurate and up-to-date responses. This agent interacts with two key tools:

    Knowledge Base: It employs RAG to retrieve relevant information on specific topics, such as company salary data.
    Wikipedia: It uses the Wikipedia API to access a wide range of information, enriching the responses with accurate and varied data.

☁️ AWS Services Used

The solution relies on several AWS services to ensure smooth integration and cost efficiency. The main services are:

    📁 S3: Stores .pdf files containing structured information that the chatbot uses to generate clear and precise responses.
    💬 Lex: Provides the user interface for the chatbot, including voice services like Amazon Transcribe and Amazon Polly.
    🧠 Bedrock: Acts as the hub for foundational model (FM) selection and hosts the knowledge base.
    ⚙ Lambda: Functions as a serverless service facilitating calls to the AI agent and its tools, offering automatic scalability, security, and flexibility.

📚 Libraries and Tools

    🦜️🔗 LangChain: Enables the integration and orchestration of different AI tools and knowledge bases, facilitating the creation of a robust AI agent.
    🌍 Wikipedia-API: Provides access to extensive and updated data from Wikipedia, enriching the chatbot's capabilities.

🚀 Functionality Description

The general flow of the chatbot is as follows:

    Event Reception: AWS Lambda receives an event from Amazon Lex.
    Response Generation: Lambda calls the AI agent that uses LangChain to process the event.
    Knowledge Base Query: The agent employs RAG to search for information in the knowledge base hosted on Amazon Bedrock.
    Access to Wikipedia: If additional information is needed, the agent queries Wikipedia using its API.
    User Response: The generated response is formatted and sent back to Amazon Lex, which presents it to the user.

