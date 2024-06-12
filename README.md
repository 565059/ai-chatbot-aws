# 🤖 ai-chatbot

_Social_

[![565059 - ai-chatbot](https://img.shields.io/badge/565059-000000?logo=github&logoColor=ffffff)](https://github.com/565059 "Ir al GitHub de 565059")

_Servicios usados_

[![Python - 3.12.0](https://img.shields.io/static/v1?label=Python&message=v3.12.0&color=3776AB&labelColor=3776AB&logo=python&logoColor=ffffff)](https://www.python.org/downloads/release/python-3120/ "Ir a Python") [![LangChain](https://img.shields.io/badge/🦜️🔗Langchain-v0.2.3-1C3C3C?&labelColor=1C3C3C)](https://github.com/langchain-ai "Ir a LangChain") [![Wikipedia-API](https://img.shields.io/badge/Wikipedia--API-v0.6.8-000000?logo=wikipedia&logoColor=ffffff&labelColor=000000)](https://github.com/martin-majlis/Wikipedia-API "Ir a Wikipedia-API") [![AWS SDK - Boto3](https://img.shields.io/badge/Boto3-v1.34.124-232f3e?logo=amazonwebservices&logoColor=ffffff&labelColor=232f3e)](https://github.com/boto/boto3 "Ir a Boto3") 

## ✏️ Resumen

Esta aplicación crea respuestas automáticas para un **chatbot** utilizando IA generativa con conexión a una base de conocimiento y a una herramienta. Para realizar dicha conexión se ha empleado Amazon Web Services y [**Boto3**](https://github.com/boto/boto3), su SDK para Python. Además se han utilizado las bibliotecas de [**LangChain**](https://github.com/langchain-ai/langchain) y de [**Wikipedia API**](https://github.com/martin-majlis/Wikipedia-API).

## 🧬 IA Generativa

Para generar las respuestas de forma automática se ha empleado el uso de [**RAG (Retrieval Augmented Generation)**](https://aws.amazon.com/what-is/retrieval-augmented-generation/) con un agente de IA. En este caso el agente creado es de tipo [**ReAct Agent**](https://react-lm.github.io/), el cual, utiliza dos herramientas para mejorar su capacidad de respuesta:

* **Base de conocimiento**: utilizando el ya mencionado [**RAG**](https://aws.amazon.com/what-is/retrieval-augmented-generation/), el agente podrá recuperar información actualizada sobre los temas que queramos que responda nuestro **chatbot**. Por ejemplo, los salarios de una empresa.  

* **Wikipedia**: utilizando su API de Python, el agente puede conectar con los servidores de Wikipedia proporcionando información sobre múltiples temas.

## ☁️ Servicios de AWS

Se ha utilizado AWS por la facilidad a la hora de realizar las conexiones entre servicios y por su bajo coste, ya que su modelo suele ser de pago por uso.

Los servicios utilizados son:

* **[Amazon S3](https://aws.amazon.com/s3):** utilizado para el almacenamiento de los archivos `.pdf` en los que se plantea la información que queremos que nuestro **chatbot** responda con claridad y exactitud.
* **[Amazon Lex](https://aws.amazon.com/lex/):** empleado para proporcionar la interfaz de usuario y la utilización de servicios de voz integrados como **Transcribe** y **Polly**.
* **[Amazon Bedrock](https://aws.amazon.com/bedrock/):** empleado como centro de selección de **modelos fundacionales (FM)** y como lugar en el que se aloja la base de conocimiento creada.
* **[Amazon Lambda](https://aws.amazon.com/lambda/):** servicio **serverless** con el que se realizan las llamadas al agente y a sus herramientas. El beneficio de este servicio es su escalabilidad automática, su seguridad y su flexibilidad.
