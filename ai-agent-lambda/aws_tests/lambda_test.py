import boto3, os, json
# from jinja2 import Template


# === LAMBDA ===
# lambda_helper = LambdaHelper()
# deploy_function
# add_lambda_trigger

# === S3 ===
# s3_helper = S3Helper()
# upload_file
# download_object
# list_objects

# === DISPLAY FILES ===
# display_helper = DisplayHelper()
# display_text_file
# display_json_file

# === NOMBRE DEL BUCKET ===
# bucket_name_text = os.environ['BUCKET_NAME_TEXT']

prompt_template = """I need to summarize a conversation. The transcript of the conversation is between the <data> XML like tags.

<data>
{{transcript}} # jinja2 template tag to insert the transcript of the conversation
</data>

The summary must contain a one word sentiment analysis, and a list of issues, problems or causes of friction
during the conversation. The output must be provided in JSON format shown in the following example. 

Example output:
{
    "version": 0.1,
    "sentiment": <sentiment>,
    "issues": [
        {
            "topic": <topic>,
            "summary": <issue_summary>,
        }
    ]
}

An `issue_summary` must only be one of:
{%- for topic in topics %} # sintaxis especial de jinja2 para ejecutar python dentro del prompt
 - `{{topic}}`
{% endfor %}

Write the JSON output and nothing more.

Here is the JSON output:"""

# === CREAR LA FUNCIÓN LAMBDA ===
s3_client = boto3.client('s3')
bedrock_runtime_client = boto3.client('bedrock-runtime', 'us-east-1')

def lambda_handler(event, context): # el evento lo crea S3 cuando metamos un objeto nuevo (un archivo)
    
    bucket = event['Records'][0]['s3']['bucket']['name'] # recogemos el bucket en el que se ha puesto el objeto
    key = event['Records'][0]['s3']['object']['key'] # recogemos el nombre del objeto
    
    # One of a few different checks to ensure we don't end up in a recursive loop.
    if "-transcript.json" not in key:
        print("This demo only works with *-transcript.json.")
        return
    
    try: 
        file_content = ""
        
        response = s3_client.get_object(Bucket=bucket, Key=key) # recoge el objeto
        
        file_content = response['Body'].read().decode('utf-8')
        
        transcript = extract_transcript_from_textract(file_content) # string de la transcripción

        print(f"Successfully read file {key} from bucket {bucket}.")

        print(f"Transcript: {transcript}")
        
        summary = bedrock_summarisation(transcript) # resumen de la conversación hecho por bedrock en json
        
        s3_client.put_object( # guarda el resumen en un nuevo objeto
            Bucket=bucket,
            Key='results.txt',
            Body=summary,
            ContentType='text/plain'
        )
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error occurred: {e}")
        }

    return {
        'statusCode': 200,
        'body': json.dumps(f"Successfully summarized {key} from bucket {bucket}. Summary: {summary}")
    }
        

# Crea una transcripción a partir del json generado por Amazon Transcript
def extract_transcript_from_textract(file_content):

    transcript_json = json.loads(file_content)

    output_text = ""
    current_speaker = None

    items = transcript_json['results']['items'] # aquí es donde se almacena cada palabra dicha por los hablantes

    # Itera sobre el contenido palabra a palabra
    for item in items:
        speaker_label = item.get('speaker_label', None) # recoge la etiqueta del hablante actual
        content = item['alternatives'][0]['content'] # recoge el contenido hablado (una palabra)
        
        # Empieza la línea con la etiqueta del hablante
        if speaker_label is not None and speaker_label != current_speaker: # si el hablante actual es diferente al hablante anterior
            current_speaker = speaker_label
            output_text += f"\n{current_speaker}: " # añade la etiqueta del hablante actual
        
        # Añade el contenido hablado
        if item['type'] == 'punctuation': # si es un punto
            output_text = output_text.rstrip()  # Quita el último espacio
        
        output_text += f"{content} " # añade el contenido hablado
        
    return output_text
        
# Bedrock resume la conversación utilizando la plantilla con jinja2
def bedrock_summarisation(transcript):
    
    with open('prompt_template.txt', "r") as file: # abre el archivo creado
        template_string = file.read()

    # Se crea el diccionario con los datos de la plantilla
    data = {
        'transcript': transcript,
        'topics': ['charges', 'location', 'availability']
    }
    
    template = Template(template_string) # crea la plantilla
    prompt = template.render(data) # hidrata la plantilla con los datos
    
    print(prompt)
    
    kwargs = {
        "modelId": "amazon.titan-text-express-v1",
        "contentType": "application/json",
        "accept": "*/*",
        "body": json.dumps(
            {
                "inputText": prompt,
                "textGenerationConfig": {
                    "maxTokenCount": 2048,
                    "stopSequences": [],
                    "temperature": 0,
                    "topP": 0.9
                }
            }
        )
    }
    
    response = bedrock_runtime_client.invoke_model(**kwargs)

    summary = json.loads(response.get('body').read()).get('results')[0].get('outputText') 
    return summary
    
# == DEPLOY FUNCTION ==
# lambda_helper.deploy_function(
#   ["lambda_function.py", "prompt_template.txt"],
#   function_name="LambdaFunctionSummarize",
# )

# === ADD LAMBDA TRIGGER ===
# lambda_helper.filter_rules_suffix = ".json" -> hace que solo se ejecute si el formato es .json
# lambda_helper.add_lambda_trigger(bucket_name_text)


# display_helper.json_file('demo-transcript.json') -> muestra el archivo

# s3_helper.upload_file(bucket_name_text,'demo-transcript.json') -> sube el archivo a S3
# s3_helper.list_objects(bucket_name_text) -> muestra los objetos en el bucket
# s3_helper.download_object(bucket_name_text, 'results.txt') -> descarga el objeto creado por la función lambda del bucket

# display_helper.text_file('results.txt') -> muestra el archivo descargado


# === LAMBDA FUNCTION PARA TRANSCRIBIR ARCHIVOS MP3===
def lambda_handler2(event, context):
    # Extract the bucket name and key from the incoming event
    bucket = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['object']['key']

    # One of a few different checks to ensure we don't end up in a recursive loop.
    if key != "dialog.mp3": 
        print("This demo only works with dialog.mp3.")
        return

    try:
        
        job_name = 'transcription-job-' + str(uuid.uuid4()) # Needs to be a unique name

        response = transcribe_client.start_transcription_job(
            TranscriptionJobName=job_name,
            Media={'MediaFileUri': f's3://{bucket}/{key}'},
            MediaFormat='mp3',
            LanguageCode='en-US',
            OutputBucketName= os.environ['S3BUCKETNAMETEXT'],  # specify the output bucket
            OutputKey=f'{job_name}-transcript.json',
            Settings={
                'ShowSpeakerLabels': True,
                'MaxSpeakerLabels': 2
            }
        )
        
    except Exception as e:
        print(f"Error occurred: {e}")
        return {
            'statusCode': 500,
            'body': json.dumps(f"Error occurred: {e}")
        }

    return {
        'statusCode': 200,
        'body': json.dumps(f"Submitted transcription job for {key} from bucket {bucket}.")
    }
