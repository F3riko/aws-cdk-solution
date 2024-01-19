import requests
import time
import boto3
import gzip
from io import BytesIO

# Replace these values with actual endpoint and buckets name from the deploy output
endpoint = "https://jb6yrmvuw3.execute-api.us-east-2.amazonaws.com/prod/"
uncompressed_bucket_name = "logfileuploadcdk-uncompressedlogbucket935c27bb-fubqmlqgpmwl"
compressed_bucket_name = "logfileuploadcdk-compressedlogbucket0653d0ce-9lowhnl1hrtb"

def decompress_gzip(data):
    with gzip.GzipFile(fileobj=BytesIO(data), mode='rb') as f:
        decompressed_data = f.read()
    return decompressed_data.decode('utf-8')

def manual_test(endpoint, uncompressed_bucket_name, compressed_bucket_name):
    try:
        # 1. Send POST to the endpoint with dummy data
        log_data = {"log": "test data"}
        response = requests.post(endpoint, json=log_data)
        assert response.status_code == 200, f"POST request failed with status code {response.status_code}"

        # Waiting for a possible delay
        time.sleep(5)

        # 2. Get newest added uncompressed object from the uncompressed bucket
        s3_client = boto3.client("s3")
        uncompressed_objects = s3_client.list_objects_v2(Bucket=uncompressed_bucket_name)['Contents']
        newest_object_key = max(uncompressed_objects, key=lambda x: x['LastModified'])['Key']
        newest_object_content_raw = s3_client.get_object(Bucket=uncompressed_bucket_name, Key=newest_object_key)['Body'].read()
        newest_object_content = newest_object_content_raw.decode('utf-8')
        assert newest_object_content == "test data", "Object content does not match expected data"

        time.sleep(5)

        # 3. Get newest added compressed object from the compressed bucket
        compressed_objects = s3_client.list_objects_v2(Bucket=compressed_bucket_name)['Contents']
        newest_compressed_object_key = max(compressed_objects, key=lambda x: x['LastModified'])['Key']
        compressed_object_content_raw = s3_client.get_object(Bucket=compressed_bucket_name, Key=newest_compressed_object_key)['Body'].read()

        # 4. Decompress and check content
        decompressed_content = decompress_gzip(compressed_object_content_raw)
        assert decompressed_content == "test data", "Decompressed object content does not match expected data"

        print("All tests were successful.")
    except Exception as e:
        print(f"Test failed: {e}")


manual_test(endpoint, uncompressed_bucket_name, compressed_bucket_name)
