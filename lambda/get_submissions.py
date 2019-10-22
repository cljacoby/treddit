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

def init_logger():
    log = logging.getLogger()
    log.setLevel(logging.INFO)
    return log

def lambda_handler(event, context):
    start = time.time()
    log = init_logger()
    bucket = s3.Bucket(BUCKET_NAME)
    bucket.download_file(KEY, TMP_FILE)
    with open(TMP_FILE) as f:
        d = json.load(f)
    end = time.time()
    duration = end - start
    log.info(f"get_submissions response time: {duration}")
    print("## print cloudwatch test")
    return d

if __name__ == "__main__":
    resp = lambda_handler(None, None)
    print(resp)

