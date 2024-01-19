import os
import gzip
import boto3
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def handler(event, context):
    try:
        logger.info("Received S3 event: {}".format(json.dumps(event)))

        # Get the bucket names from env
        compressed_bucket_name = os.environ['COMPRESSED_BUCKET_NAME']
        uncompressed_bucket_name = os.environ['UNCOMPRESSED_BUCKET_NAME']

        # Get the uncompressed log file key from bucket event
        key = event['Records'][0]['s3']['object']['key']

        logger.info("Processing log file with key: {}".format(key))

        # Read the uncompressed log file
        s3 = boto3.client('s3')
        response = s3.get_object(Bucket=uncompressed_bucket_name, Key=key)
        uncompressed_content = response['Body'].read()

        # Compress the log file content
        compressed_content = gzip.compress(uncompressed_content)

        # Upload the compressed content to the compressed bucket
        compressed_key = 'logs/{}.gz'.format(context.aws_request_id)
        logger.info("Uploading compressed content to {}: {}".format(compressed_bucket_name, compressed_key))
        s3.put_object(Bucket=compressed_bucket_name, Key=compressed_key, Body=compressed_content)

        logger.info("Log successfully compressed and stored!")

    except Exception as e:
        logger.error("Error during compression: {}".format(str(e)))
        raise e
