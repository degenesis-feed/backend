from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def ping():
    # Health check, easily test that api is live
    return "pong"

@app.get("/feed/{wallet}")
def get_feed()

@app.get("/following/{wallet}")
def get_following()

@app.get("/followers/{wallet}")
def get_followers()

@app.get("/profile/{wallet}")
def get_profile()

@app.get("/communities")
def get_communities()

