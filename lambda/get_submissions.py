import json
import boto3
import botocore

BUCKET_NAME = "treddit"
KEY = "file.txt"

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    s3.Bucket(BUCKET_NAME)
    return {
        "boto3": "test",
        'statusCode': 200,
        'event': json.dumps(event),
        'body': json.dumps('Hello from Lambda!')
    }

