import os
import json
import boto3

def handler(event, context):
    # Get the log content from the API Gateway event
    log_content = json.loads(event['body'])['log']

    # Get the bucket name from env
    uncompressed_bucket_name = os.environ['UNCOMPRESSED_BUCKET_NAME']

    # Upload the log content to the uncompressed bucket
    s3 = boto3.client('s3')
    s3.put_object(Bucket=uncompressed_bucket_name, Key=f'logs/{context.aws_request_id}.txt', Body=log_content)

    # Return a response
    return {
        'statusCode': 200,
        'body': json.dumps('Log successfully received and stored!')
    }
