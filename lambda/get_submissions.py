import json

def lambda_handler(event, context):
    return {
        'statusCode': 200,
        'event': json.dumps(event),
        'body': json.dumps('Hello from Lambda!')
    }

