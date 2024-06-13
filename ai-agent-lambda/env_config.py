import os
import boto3

# Setting the AWS region name, defaulting to 'us-east-1' if the environment variable is not set
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")

# Setting the model ID, defaulting to 'anthropic.claude-v2:1' if the environment variable is not set
MODEL_ID = os.getenv("MODEL_ID", "anthropic.claude-v2:1")

# Retrieving the knowledge base ID from the environment, no default provided
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")

# Setting the temperature for the language model, controlling randomness. Default is 0.5.
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.5"))

# Setting the top_k parameter, limiting the number of top predictions considered. Default is 50.
TOP_K = int(os.getenv("TOP_K", "50"))

# Setting the top_p parameter, controlling the cumulative probability for token selection. Default is 0.9.
TOP_P = float(os.getenv("TOP_P", "0.9"))

# Setting the maximum number of tokens to be generated. Default is 3000.
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "3000"))

# Setting the number of results to retrieve from the knowledge base. Default is 4.
RESULTS_NUMBER = int(os.getenv("RESULTS_NUMBER", "4"))

# Creating a new boto3 session with the specified AWS region
BOTO3_SESSION = boto3.Session(region_name=REGION_NAME)

# Creating a client for the 'bedrock-runtime' service within the specified region
BEDROCK_CLIENT = BOTO3_SESSION.client("bedrock-runtime", region_name=REGION_NAME)
