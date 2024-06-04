import os
import boto3

REGION_NAME = os.getenv("AWS_REGION", "us-east-1")
MODEL_ID = os.getenv("MODEL_ID","anthropic.claude-3-sonnet-20240229-v1:0")
KNOWLEDGE_BASE_ID = os.getenv("KNOWLEDGE_BASE_ID", "X4D9VAAAV5")

TEMPERATURE = float(os.getenv("TEMPERATURE", "0.5"))
TOP_K = int(os.getenv("TOP_K", "25"))
MAX_TOKENS = int(os.getenv("MAX_TOKENS", "3000"))

RESULTS_NUMBER = int(os.getenv("RESULTS_NUMBER", "15"))

BOTO3_SESSION = boto3.Session(region_name=REGION_NAME)
BEDROCK_CLIENT = BOTO3_SESSION.client("bedrock-runtime")
