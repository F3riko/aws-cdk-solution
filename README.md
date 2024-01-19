## AWS CDK Log File Upload Solution

![image](https://github.com/F3riko/aws-cdk-solution/assets/75631868/3829f2c5-f031-46e1-8567-57d8c828f5fd)

This repository contains an AWS CDK solution for log file uploads, auto-compression, and storage. The solution includes an API Gateway and Lambda functions to handle log file content, storing it in both uncompressed and compressed S3 buckets.

### AWS CDK Stack Components

#### S3 Buckets

- **UncompressedLogBucket**: Bucket for storing uncompressed log files
- **CompressedLogBucket**: Bucket for storing compressed log files

#### Lambda Functions

- **LogProcessor**: Processes log file content and stores it in the `UncompressedLogBucket`.
- **LogCompressor**: Compresses log file and stores it in the `CompressedLogBucket`.

#### API Gateway

- **LogFileUploadAPI**: API Gateway to receive log file content via HTTP POST requests.

#### CDK Outputs

- **UncompressedBucketNameOutput**: Output containing the name of the `UncompressedLogBucket`.
- **CompressedBucketNameOutput**: Output containing the name of the `CompressedLogBucket`.

### Deploying the Infrastructure

1. **Ensure AWS CLI is configured with the required credentials.**
1. **Install CDK**
1. **Deploy**: In the root directory, run the following command:

   ```bash
   cdk deploy
   ```

   This will deploy the CDK stack to your AWS account.

1. **Access Outputs**: After successful deployment, the CDK stack outputs will display the names of the S3 buckets created. The outputs can be used for manual testing.

### Testing the System

#### Unit Testing

Run unit tests using the provided `TestLogFileUploadCDK` class:

```bash
python -m unittest test_log_file_upload_cdk.py
```

The unit tests validate the existence of essential components: S3 buckets and Lambda functions, ensuring their proper creation during deployment.

#### Manual Testing

For manual testing you should manually provide values to `manual_test.py` file from the console output after deployment: endpoint, compressed and uncompressed bucket names.
Execute manual tests to verify end-to-end functionality:

```bash
python manual_test.py
```

This script sends a test log file to the API Gateway, checks the uncompressed S3 bucket for the raw log, and the compressed S3 bucket for the compressed log.

### Cleaning Up

```bash
cdk destroy
```
