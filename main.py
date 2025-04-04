from fastapi import FastAPI
from v1.processors.profile import Profile

app = FastAPI()


@app.get("/ping")
def ping():
    # Health check, easily test that api is live
    return "pong"


@app.get("/feed/{wallet}")
def get_feed():
    pass


@app.get("/following/{wallet}")
def get_following():
    pass


@app.get("/followers/{wallet}")
def get_followers():
    pass


@app.get("/profile/{wallet}")
def get_profile():
    pass


@app.post("/signUp/{wallet}")
def sign_up():
    pass


@app.get("/communities")
def get_communities():
    pass


@app.post("/addContract")
def add_contract():
    pass


@app.post("/interactWithContract")
def interact_with_contract():
    pass
