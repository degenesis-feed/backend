from fastapi import FastAPI, Request, WebSocket
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from v1.utils.entity_lookup import EntityLookup
from v1.processors.profile import Profile, profile_of
from v1.utils.feedme_status import Error as FeedMeError
from v1.processors.curvegrid import make_contract_instance
from typing import List

from nodit import Nodit


#     ___    ____  ____
#    /   |  / __ \/  _/
#   / /| | / /_/ // /
#  / ___ |/ ____// /
# /_/  |_/_/   /___/

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

nodit = Nodit()


@app.exception_handler(FeedMeError)
async def custom_error_handler(request: Request, exc: FeedMeError):
    exc.log()
    return JSONResponse(
        status_code=400, content={"error": exc.message, "details": exc.value}
    )


@app.get("/v1/ping")
def ping():
    # Health check, easily test that api is live
    return "pong"


#     ______________________     _____ __  ____________
#    / ____/ ____/ ____/ __ \   / ___// / / /  _/_  __/
#   / /_  / __/ / __/ / / / /   \__ \/ /_/ // /  / /
#  / __/ / /___/ /___/ /_/ /   ___/ / __  // /  / /
# /_/   /_____/_____/_____/   /____/_/ /_/___/ /_/


@app.get("/v1/feed/{wallet}")
def get_feed(wallet: str):
    profile = profile_of(wallet)
    addresses = get_following(wallet)
    transactions = []
    for address in addresses:
        items = nodit.get_historical(address=address)
        for item in items:
            transactions.append(item)
    return transactions


# Nodit webhook function
@app.post("/v1/feedListen")
def listen_to_feed():
    pass


#     ____  ____  ____  ____________    ______   _____   ____________
#    / __ \/ __ \/ __ \/ ____/  _/ /   / ____/  /  _/ | / / ____/ __ \
#   / /_/ / /_/ / / / / /_   / // /   / __/     / //  |/ / /_  / / / /
#  / ____/ _, _/ /_/ / __/ _/ // /___/ /___   _/ // /|  / __/ / /_/ /
# /_/   /_/ |_|\____/_/   /___/_____/_____/  /___/_/ |_/_/    \____/
#    __________________________________  _____
#   / ____/ ____/_  __/_  __/ ____/ __ \/ ___/
#  / / __/ __/   / /   / / / __/ / /_/ /\__ \
# / /_/ / /___  / /   / / / /___/ _, _/___/ /
# \____/_____/ /_/   /_/ /_____/_/ |_|/____/


@app.get("/v1/following/{wallet}")
def get_following(wallet: str) -> list[str]:
    return profile_of(wallet).following


@app.get("/v1/followers/{wallet}")
def get_followers(wallet: str) -> list[str]:
    return profile_of(wallet).followers


@app.get("/v1/profile/{wallet}")
def get_profile(wallet: str) -> dict:
    return profile_of(wallet).__dict__


#  _       _____    __    __    ____________
# | |     / /   |  / /   / /   / ____/_  __/
# | | /| / / /| | / /   / /   / __/   / /
# | |/ |/ / ___ |/ /___/ /___/ /___  / /
# |__/|__/_/  |_/_____/_____/_____/ /_/
#     ___   ____________________  _   _______
#    /   | / ____/_  __/  _/ __ \/ | / / ___/
#   / /| |/ /     / /  / // / / /  |/ /\__ \
#  / ___ / /___  / / _/ // /_/ / /|  /___/ /
# /_/  |_\____/ /_/ /___/\____/_/ |_//____/


@app.post("/v1/signUp")
def sign_up(wallet: str, description: str):
    res = Profile(wallet).new(description)
    if isinstance(res, FeedMeError):
        raise res
    else:
        return res


@app.post("/v1/follow")
def follow(follower: str, who_to_follow: str, profile_or_community: str):
    follow_entity = EntityLookup.from_string(profile_or_community)

    follower_profile = profile_of(follower)
    if follow_entity == EntityLookup.PROFILE:
        res = follower_profile.follow_profile(who_to_follow)
    elif follow_entity == EntityLookup.COMMUNITY:
        res = follower_profile.follow_community(who_to_follow)

    if isinstance(res, FeedMeError):
        raise res
    else:
        return res


@app.post("/v1/unfollow")
def unfollow(unfollower: str, who_to_unfollow: str, profile_or_community: str):
    unfollow_entity = EntityLookup.from_string(profile_or_community)
    unfollower_profile = profile_of(unfollower)

    if unfollow_entity == EntityLookup.PROFILE:
        res = unfollower_profile.follow_profile(who_to_unfollow)
    elif unfollow_entity == EntityLookup.COMMUNITY:
        res = unfollower_profile.follow_community(who_to_unfollow)

    if isinstance(res, FeedMeError):
        raise res
    else:
        return res


#    __________  _   ____________  ___   ____________
#   / ____/ __ \/ | / /_  __/ __ \/   | / ____/_  __/
#  / /   / / / /  |/ / / / / /_/ / /| |/ /     / /
# / /___/ /_/ / /|  / / / / _, _/ ___ / /___  / /
# \____/\____/_/ |_/ /_/ /_/ |_/_/  |_\____/ /_/
#     ___   ____________________  _   _______
#    /   | / ____/_  __/  _/ __ \/ | / / ___/
#   / /| |/ /     / /  / // / / /  |/ /\__ \
#  / ___ / /___  / / _/ // /_/ / /|  /___/ /
# /_/  |_\____/ /_/ /___/\____/_/ |_//____/


# Curvegrid
@app.post("/v1/addContract")
def add_contract(contract_address: str):
    res = make_contract_instance(contract_address)

    if isinstance(res, FeedMeError):
        raise res
    else:
        return res


# Curvegrid
@app.post("/v1/interactWithContract")
def interact_with_contract(
    wallet: str, contract_address: str, method: str, args: list[str]
):
    pass


#    __________  __  _____  _____  ___   ___________________________
#   / ____/ __ \/  |/  /  |/  / / / / | / /  _/_  __/  _/ ____/ ___/
#  / /   / / / / /|_/ / /|_/ / / / /  |/ // /  / /  / // __/  \__ \
# / /___/ /_/ / /  / / /  / / /_/ / /|  // /  / / _/ // /___ ___/ /
# \____/\____/_/  /_/_/  /_/\____/_/ |_/___/ /_/ /___/_____//____/


@app.get("/v1/communities")
def get_communities():
    pass


# Websocket/webhook


class ConnectionManager:
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)


manager = ConnectionManager()

#  _       ____________ _____ ____  ________ __ ____________
# | |     / / ____/ __ ) ___// __ \/ ____/ //_// ____/_  __/
# | | /| / / __/ / __  \__ \/ / / / /   / ,<  / __/   / /   
# | |/ |/ / /___/ /_/ /__/ / /_/ / /___/ /| |/ /___  / /    
# |__/|__/_____/_____/____/\____/\____/_/ |_/_____/ /_/     


@app.websocket("/ws/{wallet}")
async def websocket_endpoint(websocket: WebSocket, wallet: str):
    await manager.connect(websocket)
    addresses = get_following(wallet)
    nodit.add_webhook(wallet, addresses)
    try:
        while True:
            await websocket.receive_text()
    except Exception:
        pass
    finally:
        manager.disconnect(websocket)
        nodit.clear_webhooks(wallet)


@app.post("/webhook/")
async def webhook_listener(request: Request):
    try:
        payload = await request.json()
        message = f"Received data: {payload}"
        await manager.broadcast(message)
        return {"status": "success", "message": "Data forwarded to WebSocket clients"}
    except Exception as e:
        return {"status": "error", "message": str(e)}
