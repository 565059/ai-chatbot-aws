# ai-chatbot

## Resumen

Esta aplicación crea respuestas automáticas para un **chatbot** utilizando IA generativa, una base de conocimiento, Amazon Web Services y las bibliotecas de [**LangChain**](https://github.com/langchain-ai/langchain) y [**Wikipedia API**](https://github.com/martin-majlis/Wikipedia-API).

_Social buttons_

[![565059 - ai-chatbot](https://img.shields.io/static/v1?label=565059&message=ai-chatbot&color=FF8900&logo=github)](https://github.com/565059/ai-chatbot "Go to GitHub repo")

## IA Generativa

Para generar las respuestas de forma automática se ha empleado el uso de [**RAG**](https://aws.amazon.com/what-is/retrieval-augmented-generation/) con un agente de IA, en este caso se ha creado un [**ReAct Agent**](https://react-lm.github.io/), el cual, utiliza dos herramientas para mejorar su capacidad de respuesta:

* **Base de conocimiento**: utilizando el ya mencionado [**RAG**](https://aws.amazon.com/what-is/retrieval-augmented-generation/), el agente podrá recuperar información actualizada sobre los temas que queramos que responda nuestro **chatbot**. Por ejemplo, la información de una empresa.  

* **Wikipedia**: utilizando su API de Python, el agente puede conectar con los servidores de Wikipedia proporcionando información sobre múltiples temas.

## Servicios de AWS

En este caso se ha decidido utilizar AWS para realizar las conexiones entre servicios, ya que, ofrece un modelo pago por uso bastante asequible y una seguridad sin comparación.

Los servicios utilizados son:

* **S3 (Simple Storage Service):** utilizado para el almacenamiento de los archivos `.pdf` en los que se plantea la información que queremos que nuestro **chatbot** responda con claridad y exactitud.
* **Lex:** empleado para proporcionar la interfaz de usuario y la utilización de servicios de voz integrados como pueden ser **Transcribe** y **Polly**.
* **Bedrock:** empleado como centro de selección de **modelos fundacionales (FM)** y como lugar en el que se aloja la base de conocimiento creada.
* **Lambda:** servicio **serverless** que se utiliza para realizar llamadas al agente y a sus herramientas. El beneficio de este servicio es su escalabilidad automática, su seguridad y su flexibilidad.
