import json

from fastapi import FastAPI
from v1.processors.profile import Profile, profile_of

app = FastAPI()


@app.get("/v1/ping")
def ping():
    # Health check, easily test that api is live
    return "pong"


@app.get("/v1/feed/{wallet}")
def get_feed(wallet: str):
    profile = profile_of(wallet)
    pass


# Nodit webhook function
@app.post("/v1/feedListen")
def listen_to_feed():
    pass


@app.get("/v1/following/{wallet}")
def get_following(wallet: str) -> list[str]:
    return json.dumps(profile_of(wallet).following)


@app.get("/v1/followers/{wallet}")
def get_followers(wallet: str) -> list[str]:
    return profile_of(wallet).followers


@app.get("/v1/profile/{wallet}")
def get_profile(wallet: str) -> dict:
    return profile_of(wallet)


@app.post("/v1/signUp")
def sign_up(wallet: str, description: str):
    Profile(wallet).new(description)


@app.get("/v1/communities")
def get_communities():
    pass


# Curvegrid
@app.post("/v1/addContract")
def add_contract():
    pass


# Curvegrid
@app.post("/v1/interactWithContract")
def interact_with_contract():
    pass
