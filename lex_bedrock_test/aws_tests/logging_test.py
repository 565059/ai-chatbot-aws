import boto3
import json
import os

bedrock_client = boto3.client('bedrock', region_name='us-east-1')

# HELPER FUNCTION FROM CLOUDWATCH
# from helpers.CloudWatchHelper import CloudWatchHelper
# cloudwatch = CloudWatchHelper()
# log_group_name = '/my/amazon/bedrock/logs'
# cloudwatch.create_log_group(log_group_name)

loggingConfig = {
    'cloudWatchConfig': {
        'logGroupName': log_group_name, # donde se ponen los logs
        'roleArn': os.environ['LOGGINGROLEARN'], # rol con permisos para crear logs en cloudwatch
        'largeDataDeliveryS3Config': { # donde se guardan los datos
            'bucketName': os.environ['LOGGINGBUCKETNAME'], # el bucket
            'keyPrefix': 'amazon_bedrock_large_data_delivery', # la "carpeta" de los datos
        }
    },
    's3Config': { # meterlo directamente en el bucket
        'bucketName': os.environ['LOGGINGBUCKETNAME'],
        'keyPrefix': 'amazon_bedrock_logs', # la "carpeta" de los logs
    },
    'textDataDeliveryEnabled': True, # el tipo de datos que le permitimos enviar
}

bedrock_client.put_model_invocation_logging_configuration(loggingConfig=loggingConfig)

bedrock_client.get_model_invocation_logging_configuration() # devuelve la configuración

# cloudwatch.print_recent_logs(log_group_name) # muestra los logs recientes de los ultimos 5 min