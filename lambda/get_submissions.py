import json
import boto3
import botocore
import time
import os

BUCKET_NAME = "treddit"
KEY = "submissions.json"
TMP_FILE = '/tmp/submissions.json'

s3 = boto3.resource('s3')

def lambda_handler(event, context):
    start = time.time()
    bucket = s3.Bucket(BUCKET_NAME)
    bucket.download_file(KEY, TMP_FILE)
    with open(TMP_FILE) as f:
        d = json.load(f)
    return d

