import os
from dotenv import load_dotenv

# Explicitly load the .env file from the server2 directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '.env'))

# Get environment variables
AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
AWS_REGION = os.getenv('AWS_REGION')
S3_BUCKET_NAME = os.getenv('S3_BUCKET_NAME')
PG_CONNECTION_STRING = os.getenv('PG_CONNECTION_STRING')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Print the values for debugging
print("AWS_ACCESS_KEY_ID:", AWS_ACCESS_KEY_ID)
print("AWS_SECRET_ACCESS_KEY:", AWS_SECRET_ACCESS_KEY)
print("AWS_REGION:", AWS_REGION)
print("S3_BUCKET_NAME:", S3_BUCKET_NAME)
print("PG_CONNECTION_STRING:", PG_CONNECTION_STRING)
print("OPENAI_API_KEY:", OPENAI_API_KEY)

# Check if any required environment variable is missing
if not AWS_ACCESS_KEY_ID or not AWS_SECRET_ACCESS_KEY or not PG_CONNECTION_STRING:
    print("Missing required environment variables. Please check your .env file.")
    raise ValueError("Missing required environment variables. Please check your .env file.")
