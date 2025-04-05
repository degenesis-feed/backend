import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.environ.get("NODIT")
if not api_key:
    print("No NODIT API Key set in .env, quitting")
    quit()
webhook_url = os.environ.get("WEBHOOK_BASE")
if not webhook_url:
    print("No WEBHOOK_BASE set in .env, quitting")
    quit()


class Nodit:
    def __init__(self, api_key):
        pass

    def _get_api_url(self, network: str, action: str) -> str:
        pass

    def get_historical(self, address: str) -> list:
        pass

    def add_webhook(self, addresses):
        pass

    def delete_webhooks(self, addresses):
        pass

    def get_webhooks(self, addresses: list[str]) -> list:
        pass


# def get_api_url()

api_url = "https://web3.nodit.io/v1/ethereum/mainnet/webhooks"


payload = {
    "eventType": "SUCCESSFUL_TRANSACTION",
    "description": "Webhook for successful transaction",
    "notification": {"webhookUrl": f"{webhook_url}"},
    "condition": {"addresses": ["0x4838b106fce9647bdf1e7877bf73ce8b0bad5f97"]},
}
headers = {
    "accept": "application/json",
    "content-type": "application/json",
    "X-API-KEY": api_key,
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)
