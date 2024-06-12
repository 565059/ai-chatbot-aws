# 🤖 ai-chatbot

[![565059 - ai-chatbot](https://img.shields.io/static/v1?label=565059&message=ai-chatbot&color=FF8900&logo=github)](https://github.com/565059/ai-chatbot "Go to GitHub repo") [![Python - 3.12.0](https://img.shields.io/static/v1?label=Python&message=3.12.0&color=3776AB&labelColor=3776AB&logo=python&logoColor=ffffff)](https://www.python.org/downloads/release/python-3120/ "Go to Python version") [![Amazon Web Services](https://img.shields.io/badge/Amazon_Web_Services-232f3e?logo=amazonwebservices&logoColor=ffffff)](https://aws.amazon.com "Go to AWS") [![LangChain](https://img.shields.io/badge/Langchain-0.2.3-1C3C3C?logo=langchain&logoColor=ffffff)](https://github.com/langchain-ai "Go to LangChain")
🦜️🔗 LangChain

## ✏️ Resumen

Esta aplicación crea respuestas automáticas para un **chatbot** utilizando IA generativa con conexión a una base de conocimiento. Para realizar dicha conexión se ha empleado Amazon Web Services y las bibliotecas de [**LangChain**](https://github.com/langchain-ai/langchain) y de [**Wikipedia API**](https://github.com/martin-majlis/Wikipedia-API).

## 🧬 IA Generativa

Para generar las respuestas de forma automática se ha empleado el uso de [**RAG**](https://aws.amazon.com/what-is/retrieval-augmented-generation/) con un agente de IA, en este caso se ha creado un [**ReAct Agent**](https://react-lm.github.io/), el cual, utiliza dos herramientas para mejorar su capacidad de respuesta:

* **Base de conocimiento**: utilizando el ya mencionado [**RAG**](https://aws.amazon.com/what-is/retrieval-augmented-generation/), el agente podrá recuperar información actualizada sobre los temas que queramos que responda nuestro **chatbot**. Por ejemplo, la información de una empresa.  

* **Wikipedia**: utilizando su API de Python, el agente puede conectar con los servidores de Wikipedia proporcionando información sobre múltiples temas.

## ☁️ Servicios de AWS

En este caso se ha decidido utilizar AWS para realizar las conexiones entre servicios, ya que, ofrece un modelo pago por uso bastante asequible y una seguridad sin comparación.

Los servicios utilizados son:

* **[Amazon S3](https://aws.amazon.com/s3):** utilizado para el almacenamiento de los archivos `.pdf` en los que se plantea la información que queremos que nuestro **chatbot** responda con claridad y exactitud.
* **[Amazon Lex](https://aws.amazon.com/lex/):** empleado para proporcionar la interfaz de usuario y la utilización de servicios de voz integrados como pueden ser **Transcribe** y **Polly**.
* **[Amazon Bedrock](https://aws.amazon.com/bedrock/):** empleado como centro de selección de **modelos fundacionales (FM)** y como lugar en el que se aloja la base de conocimiento creada.
* **[Amazon Lambda](https://aws.amazon.com/lambda/):** servicio **serverless** que se utiliza para realizar llamadas al agente y a sus herramientas. El beneficio de este servicio es su escalabilidad automática, su seguridad y su flexibilidad.
