import os
import requests
from dotenv import load_dotenv
from v1.utils.feedme_status import FeedMeStatus

load_dotenv()

CGURL = os.getenv("CURVEGRID_URL") 
CGJWT = os.getenv("CURVEGRID_JWT")
CHAIN = "base"

def make_contract_instance(address: str) -> FeedMeStatus:
    query = {"include": "contractLookup"}
    final_url = f"https://{CGURL}/api/v0/chains/{CHAIN}/addresses/{address}"

    header = {"Authorization": f"Bearer {CGJWT}"}

    res = requests.get(final_url, params=query, headers=header)

    return FeedMeStatus.SUCCESS.create("Address info: ", res.json)

