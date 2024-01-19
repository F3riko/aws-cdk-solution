import unittest
from aws_cdk import App
from log_upload_cdk.log_upload_cdk_stack import LogFileUploadCDK

class TestLogFileUploadCDK(unittest.TestCase):

    def setUp(self):
        self.app = App()
        self.stack = LogFileUploadCDK(self.app, "TestStack")

    def test_s3_buckets_exist(self):
        uncompressed_bucket = self.stack.node.find_child('UncompressedLogBucket')
        compressed_bucket = self.stack.node.find_child('CompressedLogBucket')
        self.assertIsNotNone(uncompressed_bucket)
        self.assertIsNotNone(compressed_bucket)

    def test_lambda_functions_exist(self):
        log_processor = self.stack.node.find_child('LogProcessor')
        log_compressor = self.stack.node.find_child('LogCompressor')
        self.assertIsNotNone(log_processor)
        self.assertIsNotNone(log_compressor)

if __name__ == '__main__':
    unittest.main()