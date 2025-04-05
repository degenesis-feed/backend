import os
import requests
from dotenv import load_dotenv
from v1.utils.feedme_status import FeedMeStatus
from db.db import get_abi, add_abi
from db.db_setup import get_connection

load_dotenv()

CGURL = os.getenv("CURVEGRID_URL")
CGJWT = os.getenv("CURVEGRID_JWT")
CHAIN = "ethereum"


def make_contract_instance(contract_address: str) -> FeedMeStatus:
    con = get_connection()
    cached_abi = get_abi(con, contract_address)
    if cached_abi:
        return FeedMeStatus.SUCCESS.create("Address info: ", cached_abi)

    query = {"include": "contractLookup"}
    final_url = f"{CGURL}/api/v0/chains/{CHAIN}/addresses/{contract_address}"

    header = {"Authorization": f"Bearer {CGJWT}"}

    res = requests.get(final_url, params=query, headers=header)
    add_abi(con, contract_address, res.text)
    return FeedMeStatus.SUCCESS.create("Address info: ", res.text)


def interact_with_contract_method(
    wallet: str, contract_address: str, method: str, args: list[str] | None
) -> FeedMeStatus:
    final_url = f"{CGURL}/api/v0/chains/{CHAIN}/addresses/{wallet}/contracts/{contract_address}/methods/{method}"

    if args:
        data = {"args": args}
        res = requests.post(final_url, json=data)
    else:
        res = requests.post(final_url)

    return FeedMeStatus.SUCCESS.create("Interaction response: ", res.text)
