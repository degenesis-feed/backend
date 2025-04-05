import json

from fastapi import FastAPI
from v1.processors.profile import Profile, profile_of
from v1.utils.feedme_status import FeedMeStatus

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
def sign_up(wallet: str, description: str) -> FeedMeStatus:
    return Profile(wallet).new(description)

@app.post("/v1/follow")
def follow(follower: str, who_to_follow: str) -> FeedMeStatus:
    follower_profile = profile_of(follower)
    return follower_profile.follow(who_to_follow)

@app.post("/v1/unfollow")
def unfollow(unfollower: str, who_to_unfollow: str) -> FeedMeStatus:
    unfollower_profile = profile_of(unfollower)
    return unfollower_profile.unfollow(who_to_unfollow)

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
