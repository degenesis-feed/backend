import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

load_dotenv()
api_key = os.environ.get("NODIT")
# if not api_key:
#     print("No NODIT API Key set in .env, quitting")
#     quit()
webhook_url = os.environ.get("WEBHOOK_BASE")
# if not webhook_url:
#     print("No WEBHOOK_BASE set in .env, quitting")
#     quit()


class Nodit:
    def __init__(self, api_key=api_key):
        self.api_key = api_key
        self.networks = ["base"]
        pass

    def _get_api_url(
        self, network: str, action: str, subscription_id: str = None
    ) -> str:
        match action:
            case "historical_transfers":
                url = "https://web3.nodit.io/v1/base/mainnet/blockchain/getTransactionsByAccount"
                # url = f"https://web3.nodit.io/v1/{network}/mainnet/token/getTokenTransfersByAccount"
                return url
            case "webhook":
                url = f"https://web3.nodit.io/v1/{network}/mainnet/webhooks"
                return url
            case "delete_webhook":
                url = f"https://web3.nodit.io/v1/{network}/mainnet/webhooks/{subscription_id}"
                return url

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
        transactions = []
        if not from_date or not to_date:
            current_time = datetime.now()
            to_date = current_time.isoformat()
            thirty_days_before = current_time - timedelta(days=30)
            from_date = thirty_days_before.isoformat()
        for network in self.networks:
            url = self._get_api_url(network=network, action="historical_transfers")
            payload = {
                "accountAddress": address,
                "fromDate": from_date,
                "toDate": to_date,
                "withCount": False,
                "withZeroValue": True,
                "relation": "from",
            }
            try:
                response = requests.post(url, json=payload, headers=headers)
                response_dict = json.loads(response.text)
                print(response_dict["items"])
                for item in response_dict["items"]:
                    if item["input"] != "0x":
                        transactions.append(item)

            except Exception:
                # avoid api limit by just skipping the rest. Needs better fix
                break
        # print(transactions)
        return transactions

    def add_webhook(self, follower_address: str, addresses: list[str]):
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-API-KEY": api_key,
        }
        for network in self.networks:
            url = self._get_api_url(network=network, action="webhook")
            payload = {
                "eventType": "SUCCESSFUL_TRANSACTION",
                "description": follower_address,
                "notification": {"webhookUrl": webhook_url},
                "condition": {"addresses": addresses},
            }

            response = requests.post(url, json=payload, headers=headers)

            print(response.text)

    def clear_webhooks(self, follower_address):
        # function to delete all webhooks for an account
        sub_ids = self.get_webhooks(follower_address=follower_address)
        headers = {"accept": "application/json", "X-API-KEY": api_key}
        for network in sub_ids:
            url = self._get_api_url(
                network=network,
                action="delete_webhook",
                subscription_id=sub_ids[network],
            )
            response = requests.delete(url, headers=headers)
        return True

    def get_webhooks(self, follower_address: str) -> list:
        """
        returns a list of subscriptionIds for webhooks that is registered to listed to the followings of a certain wallet
        """
        headers = {"accept": "application/json", "X-API-KEY": api_key}
        webhooks = {}
        for network in self.networks:
            url = self._get_api_url(network=network, action="webhook")
            response = requests.get(url, headers=headers)
            network_webhooks = json.loads(response.text)["items"]
            for webhook in network_webhooks:
                if webhook["description"] == follower_address:
                    webhooks[network] = webhook["subscriptionId"]
        return webhooks


# def get_api_url()
n = Nodit(api_key=api_key)
# n.get_historical("0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
# n.add_webhook(
#     follower_address="0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb",
#     addresses=["0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045"],
# )
# w = n.get_webhooks(follower_address="0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb")
# w = n.get_webhooks(follower_address="0xd8dA6BF26964aF9D7eEd9e03E53415D37aA96045")
# print(w)


# n.clear_webhooks(follower_address="0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb")
