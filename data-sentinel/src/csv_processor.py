import boto3

class CSVProcessor:
    def __init__(self, sensitive_data_identifier):
        self.s3 = boto3.client('s3')
        self.sensitive_data_identifier = sensitive_data_identifier

    def process(self, bucket, key):
        # Baixa o arquivo do S3
        obj = self.s3.get_object(Bucket=bucket, Key=key)
        content = obj['Body'].read().decode('utf-8')
        result = self.sensitive_data_identifier.identify(content)
        return result