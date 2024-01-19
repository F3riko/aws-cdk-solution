from aws_cdk import Stack, CfnOutput
from aws_cdk.aws_apigateway import RestApi, LambdaIntegration
from aws_cdk.aws_s3 import Bucket, EventType
from aws_cdk.aws_lambda import Function, Runtime, Code
from aws_cdk.aws_s3_notifications import LambdaDestination

class LogFileUploadCDK(Stack):
    def __init__(self, scope, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        # S3 buckets
        uncompressed_bucket = Bucket(self, "UncompressedLogBucket")
        compressed_bucket = Bucket(self, "CompressedLogBucket")

        # Lambda function to process log content
        log_processor = Function(
            self, "LogProcessor",
            runtime=Runtime.PYTHON_3_8,
            handler="log_processor.handler",
            code=Code.from_asset("lambda"),
            environment={
                'UNCOMPRESSED_BUCKET_NAME': uncompressed_bucket.bucket_name,
            }
        )

        # Grant Lambda permission to write to uncompressed bucket
        uncompressed_bucket.grant_write(log_processor)

        # Lambda function to compress log file from uncompressed bucket
        log_compressor = Function(
            self, "LogCompressor",
            runtime=Runtime.PYTHON_3_8,
            handler="log_compressor.handler",
            code=Code.from_asset("lambda"),
            environment={
                'UNCOMPRESSED_BUCKET_NAME': uncompressed_bucket.bucket_name,
                'COMPRESSED_BUCKET_NAME': compressed_bucket.bucket_name
            }
        )

        # Grant Lambda permission to write to compressed bucket and read from uncompressed bucket
        uncompressed_bucket.grant_read(log_compressor)
        compressed_bucket.grant_write(log_compressor)

        # API Gateway and Lambda integration
        api = RestApi(self, "LogFileUploadAPI")
        integration = LambdaIntegration(log_processor)
        api.root.add_method("POST", integration)

        # Configure event notification for the uncompressed bucket to trigger
        # compressor function after each upload
        uncompressed_bucket.add_event_notification(
            EventType.OBJECT_CREATED,
            LambdaDestination(log_compressor)
        )
        
        # Bucket names for manual testing purposes
        CfnOutput(self, "UncompressedBucketNameOutput", value=uncompressed_bucket.bucket_name)
        CfnOutput(self, "CompressedBucketNameOutput", value=compressed_bucket.bucket_name)