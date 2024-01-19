#!/usr/bin/env python3
import os

import aws_cdk as cdk

from log_upload_cdk.log_upload_cdk_stack import LogFileUploadCDK


app = cdk.App()
LogFileUploadCDK(app, "LogFileUploadCDK",)

app.synth()
