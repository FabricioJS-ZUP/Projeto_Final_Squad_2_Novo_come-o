import requests

class StackSpotQuickCommandClient:
    def __init__(self, api_url, token):
        self.api_url = api_url
        self.token = token

    def run_quick_command(self, csv_content):
        payload = {
            "input_data": csv_content
        }
        headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }
        response = requests.post(self.api_url, json=payload, headers=headers)
        response.raise_for_status()
        return response.json()