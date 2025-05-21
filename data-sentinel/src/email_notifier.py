import boto3

class EmailNotifier:
    def __init__(self, sender_email):
        self.ses = boto3.client('ses')
        self.sender_email = sender_email

    def send_email(self, recipient, subject, body):
        self.ses.send_email(
            Source=self.sender_email,
            Destination={'ToAddresses': [recipient]},
            Message={
                'Subject': {'Data': subject},
                'Body': {'Text': {'Data': body}}
            }
        )