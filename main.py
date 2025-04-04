from fastapi import FastAPI
from v1.processors.profile import Profile, profile_of

app = FastAPI()


@app.get("/ping")
def ping():
    # Health check, easily test that api is live
    return "pong"


@app.get("/feed/{wallet}")
def get_feed():
    pass


@app.get("/following/{wallet}")
def get_following(wallet: str) -> list[str]:
    return profile_of(wallet).following


@app.get("/followers/{wallet}")
def get_followers(wallet: str) -> list[str]:
    return profile_of(wallet).followers


@app.get("/profile/{wallet}")
def get_profile(wallet: str) -> Profile:
    return profile_of(wallet)


@app.post("/signUp/")
def sign_up(wallet: str, description: str):
    profile = Profile(wallet)
    profile.new(description)


@app.get("/communities")
def get_communities():
    pass


@app.post("/addContract")
def add_contract():
    pass


@app.post("/interactWithContract")
def interact_with_contract():
    pass
