from datetime import datetime, timedelta
import json
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
        self.api_key = api_key
        self.networks = ["base", "ethereum"]
        pass

    def _get_api_url(self, network: str, action: str) -> str:
        match action:
            case "historical_transfers":
                url = f"https://web3.nodit.io/v1/{network}/mainnet/token/getTokenTransfersByAccount"
                return url
        # url = "https://web3.nodit.io/v1/arbitrum/mainnet/token/getTokenTransfersByAccount"

        pass

    def get_historical(
        self, address: str, from_date: str = "", to_date: str = ""
    ) -> list:
        """
        Get historical token transfers for a wallet address
        If no from_date and to_date is specified, defaults to last 30 days
        """
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": self.api_key,
        }
        transactions = {}
        for network in self.networks:
            transactions[network] = []
            url = self._get_api_url(network=network, action="historical_transfers")
            if not from_date or not to_date:
                current_time = datetime.now()
                to_date = current_time.isoformat()
                thirty_days_before = current_time - timedelta(days=30)
                from_date = thirty_days_before.isoformat()
            payload = {
                "accountAddress": address,
                "fromDate": from_date,
                "toDate": to_date,
                "withCount": False,
                "withZeroValue": False,
            }
            response = requests.post(url, json=payload, headers=headers)
            response_dict = json.loads(response.text)
            transactions[network] = response_dict["items"]
        # print(transactions)
        return transactions

    def add_webhook(self, addresses):
        pass

    def delete_webhooks(self, addresses):
        pass

    def get_webhooks(self, addresses: list[str]) -> list:
        pass


# def get_api_url()
# n = Nodit(api_key=api_key)
# n.get_historical("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")

# payload = {
#     "eventType": "SUCCESSFUL_TRANSACTION",
#     "description": "Webhook for successful transaction",
#     "notification": {"webhookUrl": f"{webhook_url}"},
#     "condition": {"addresses": ["0x4838b106fce9647bdf1e7877bf73ce8b0bad5f97"]},
# }
# headers = {
#     "accept": "application/json",
#     "content-type": "application/json",
#     "X-API-KEY": api_key,
# }

# response = requests.post(url, json=payload, headers=headers)

# print(response.text)
