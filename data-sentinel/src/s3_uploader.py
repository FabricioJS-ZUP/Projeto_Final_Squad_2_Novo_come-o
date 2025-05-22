import boto3

class S3Uploader:
    def __init__(self, bucket_name):
        self.s3 = boto3.client('s3')
        self.bucket_name = bucket_name

    def upload_file(self, file_path, object_name):
        self.s3.upload_file(file_path, self.bucket_name, object_name)