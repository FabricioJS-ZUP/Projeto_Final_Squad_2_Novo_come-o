class SensitiveDataIdentifier:
    def __init__(self, stackspot_client):
        self.stackspot_client = stackspot_client

    def identify(self, csv_content):
        return self.stackspot_client.run_quick_command(csv_content)
    