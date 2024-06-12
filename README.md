![awslambda](https://github.com/565059/ai-chatbot/assets/118855900/4a20fe65-583e-4bef-8008-bab4dea65ec7)![awslambda](https://github.com/565059/ai-chatbot/assets/118855900/345dbaff-98ad-48e6-abd1-b29c3b8198ea)# 🤖 ai-chatbot

_Social_

[![565059 - ai-chatbot](https://img.shields.io/badge/565059-000000?logo=github&logoColor=ffffff)](https://github.com/565059 "Go to 565059's GitHub")

_Services used_

[![Python - 3.12.0](https://img.shields.io/static/v1?label=Python&message=v3.12.0&color=3776AB&labelColor=3776AB&logo=python&logoColor=ffffff)](https://www.python.org/downloads/release/python-3120/ "Go to Python") [![LangChain](https://img.shields.io/badge/🦜️🔗Langchain-v0.2.3-1C3C3C?&labelColor=1C3C3C)](https://github.com/langchain-ai "Go to LangChain") [![Wikipedia-API](https://img.shields.io/badge/Wikipedia--API-v0.6.8-000000?logo=wikipedia&logoColor=ffffff&labelColor=000000)](https://github.com/martin-majlis/Wikipedia-API "Go to Wikipedia-API") [![AWS SDK - Boto3](https://img.shields.io/badge/Boto3-v1.34.124-232f3e?logo=amazonwebservices&logoColor=ffffff&labelColor=232f3e)](https://github.com/boto/boto3 "Go to Boto3") 

## ✏️ Summary

Esta aplicación crea respuestas automáticas para un **chatbot** utilizando IA generativa con conexión a una base de conocimiento y a una herramienta. Para realizar dicha conexión se ha empleado Amazon Web Services y [**Boto3**](https://github.com/boto/boto3), su SDK para Python. Además se han utilizado las bibliotecas de [**LangChain**](https://github.com/langchain-ai/langchain) y de [**Wikipedia API**](https://github.com/martin-majlis/Wikipedia-API).

## 🧬 Generative IA

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


![Uploa<svg role="img" viewBox="0 0 24 24" xmlns="http://www.w3.org/2000/svg">
<title>AWS Lambda</title><path fill="#FF9900" d="M4.9855 0c-.2941.0031-.5335.2466-.534.5482L4.446 5.456c0 .1451.06.2835.159.3891a.5322.5322 0 0 0 .3806.1562h3.4282l8.197 17.6805a.5365.5365 0 0 0 .4885.3181h5.811c.2969 0 .5426-.2448.5426-.5482V18.544c0-.3035-.2392-.5482-.5425-.5482h-2.0138L12.7394.3153C12.647.124 12.4564 0 12.2452 0h-7.254Zm.5397 1.0907h6.3678l8.16 17.6804a.5365.5365 0 0 0 .4885.3181h1.8178v3.8173H17.437L9.2402 5.226a.536.536 0 0 0-.4885-.318H5.5223Zm2.0137 8.2366c-.2098.0011-.3937.1193-.4857.3096L.6002 23.2133a.5506.5506 0 0 0 .0313.5282.5334.5334 0 0 0 .4544.25h6.169a.5468.5468 0 0 0 .497-.3096l3.38-7.166a.5405.5405 0 0 0-.0029-.4686L8.036 9.637a.5468.5468 0 0 0-.4942-.3096Zm.0057 1.8036 2.488 5.1522-3.1214 6.6206H1.9465Z"/></svg>ding awslambda.svg…]()

🤖 AI Chatbot con AWS y LangChain
📋 Resumen

Este proyecto crea un chatbot inteligente que genera respuestas automáticas utilizando inteligencia artificial generativa y una base de conocimiento dinámica. La solución integra varios servicios de Amazon Web Services (AWS) y utiliza las bibliotecas de LangChain y la API de Wikipedia para enriquecer las respuestas.
🧠 IA Generativa con RAG

Se ha implementado un agente de IA de tipo ReAct Agent que utiliza la técnica de Retrieval Augmented Generation (RAG) para proporcionar respuestas precisas y actualizadas. Este agente interactúa con dos herramientas clave:

    Base de conocimiento: Emplea RAG para recuperar información relevante sobre temas específicos, como por ejemplo, datos salariales de una empresa.
    Wikipedia: Usa la API de Wikipedia para acceder a una amplia gama de información, enriqueciendo las respuestas con datos precisos y variados.

☁️ Servicios de AWS Utilizados

La solución se apoya en varios servicios de AWS para garantizar una integración fluida y un costo eficiente. Los servicios principales son:

* [**📁 S3**](https://aws.amazon.com/s3): Almacena los archivos .pdf que contienen la información estructurada que el chatbot utiliza para generar respuestas claras y precisas.
* [**💬 Lex**](https://aws.amazon.com/lex/): Proporciona la interfaz de usuario para el chatbot, incluyendo servicios de voz como Amazon Transcribe y Amazon Polly.
* [**🧠 Bedrock**](https://aws.amazon.com/bedrock/): Actúa como el centro de selección de modelos fundacionales (FM) y alberga la base de conocimiento.
* [** Lambda**](https://aws.amazon.com/lambda/): Funciona como un servicio serverless que facilita las llamadas al agente de IA y sus herramientas, ofreciendo escalabilidad automática, seguridad y flexibilidad.
<img alt="lambda" src="https://github.com/565059/ai-chatbot/assets/118855900/7d040384-d65d-47b8-9b66-20441fa33d96" width="15" height="auto">

📚 Bibliotecas y Herramientas

    LangChain: Permite la integración y orquestación de diferentes herramientas de IA y bases de conocimiento, facilitando la creación de un agente de IA robusto.
    Wikipedia API: Proporciona acceso a datos extensos y actualizados de Wikipedia, enriqueciendo las capacidades del chatbot.

🚀 Descripción del Funcionamiento

El flujo general del chatbot es el siguiente:

* **Recepción del Evento**: AWS Lambda recibe un evento de Amazon Lex.
* **Generación de la Respuesta**: Lambda llama al agente de IA que utiliza LangChain para procesar el evento.
* **Consulta a la Base de Conocimiento**: El agente emplea RAG para buscar información en la base de conocimiento alojada en Amazon Bedrock.
* **Acceso a Wikipedia**: En caso de requerir información adicional, el agente consulta la Wikipedia utilizando su API.
    Respuesta al Usuario: La respuesta generada se envía de vuelta a Amazon Lex, que la presenta al usuario.
