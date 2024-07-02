import os  # Importing the os module for environment variables
import boto3  # Importing boto3 for AWS SDK

# Default values or values fetched from environment variables
REGION_NAME = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("MODEL_ID", "anthropic.claude-v2:1")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID")

# Model parameters fetched from environment variables with default values
TEMPERATURE = float(os.getenv("TEMPERATURE", "0.5"))  # Randomness
TOP_K = int(os.getenv("TOP_K", "50"))  # Limits predictions
TOP_P = float(os.getenv("TOP_P", "0.9"))  # Probability of generated tokens
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "3000"))  # Limits the number of tokens
MODEL_TEMPLATE = (os.getenv("MODEL_TEMPLATE"))

# Number of results from the knowledge base fetched from environment variables with default value
RESULTS_NUMBER = int(os.getenv("RESULTS_NUMBER", "4"))

# Creating a boto3 session with specified region
BOTO3_SESSION = boto3.Session(region_name=REGION_NAME)

# Creating a Bedrock Runtime client using the boto3 session
BEDROCK_CLIENT = BOTO3_SESSION.client("bedrock-runtime", region_name=REGION_NAME)
