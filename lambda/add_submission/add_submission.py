import json
import boto3
import botocore
import time
import os
import logging

BUCKET_NAME = "treddit"
KEY = "submissions.json"
TMP_FILE = '/tmp/submissions.json'

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    print("## event")
    print(event)
    print("## context")
    print(context)
    return {
        "test": 123        
    }
    
if __name__ == "__main__":
    resp = lambda_handler(None, None)
    print(resp)
