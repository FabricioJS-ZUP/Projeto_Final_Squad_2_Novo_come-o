class S3EventHandler:
    def __init__(self, csv_processor):
        self.csv_processor = csv_processor

    def handle(self, event):
        # event: dict vindo do trigger do S3
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        return self.csv_processor.process(bucket, key)