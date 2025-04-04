from fastapi import FastAPI

app = FastAPI()

@app.get("/ping")
def ping():
    # Health check, easily test that api is live
    return "pong"

@app.get("/feed")
def get_feed()

@app.get("/following")
def get_following()

@app.get("/followers")
def get_followers()

@app.get("/communities")
def get_communities

