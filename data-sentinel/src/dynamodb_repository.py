import boto3

class DynamoDBRepository:
    def __init__(self, table_name):
        self.dynamodb = boto3.resource('dynamodb')
        self.table = self.dynamodb.Table(table_name)

    def save_result(self, result):
        self.table.put_item(Item=result)