import boto3
from fastapi import HTTPException
from server2.config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION


# S3 client setup
s3_client = boto3.client(
    's3', 
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    region_name=AWS_REGION
)

def upload_to_s3(file, bucket_name: str):
    try:
        s3_client.upload_fileobj(file.file, bucket_name, file.filename)
        s3_url = f'https://{bucket_name}.s3.{AWS_REGION}.amazonaws.com/{file.filename}'
        return s3_url
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error uploading to S3: {str(e)}")
