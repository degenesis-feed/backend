from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from v1.utils.entity_lookup import EntityLookup
from v1.processors.profile import Profile, profile_of
from v1.utils.feedme_status import Error as FeedMeError
from v1.processors.curvegrid import make_contract_instance

from nodit import Nodit


#     ___    ____  ____
#    /   |  / __ \/  _/
#   / /| | / /_/ // /
#  / ___ |/ ____// /
# /_/  |_/_/   /___/

app = FastAPI()
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
    pass


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
def follow(follower: str, who_to_follow: str, profile_or_wallet: str):
    follow_entity = EntityLookup.from_string(profile_or_wallet)

    follower_profile = profile_of(follower)
    if isinstance(follow_entity, EntityLookup.PROFILE):
        res = follower_profile.follow_profile(who_to_follow)
    elif isinstance(follow_entity, EntityLookup.COMMUNITY):
        res = follower_profile.follow_community(who_to_follow)

    if isinstance(res, FeedMeError):
        raise res
    else:
        return res


@app.post("/v1/unfollow")
def unfollow(unfollower: str, who_to_unfollow: str, profile_or_wallet: str):
    unfollow_entity = EntityLookup.from_string(profile_or_wallet)
    unfollower_profile = profile_of(unfollower)

    if isinstance(unfollow_entity, EntityLookup.PROFILE):
        res = unfollower_profile.follow_profile(who_to_unfollow)
    elif isinstance(unfollow_entity, EntityLookup.COMMUNITY):
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
def add_contract(address: str):
    res = make_contract_instance(address)

    if isinstance(res, FeedMeError):
        raise res
    else:
        return res


# Curvegrid
@app.post("/v1/interactWithContract")
def interact_with_contract():
    pass


#    __________  __  _____  _____  ___   ___________________________
#   / ____/ __ \/  |/  /  |/  / / / / | / /  _/_  __/  _/ ____/ ___/
#  / /   / / / / /|_/ / /|_/ / / / /  |/ // /  / /  / // __/  \__ \
# / /___/ /_/ / /  / / /  / / /_/ / /|  // /  / / _/ // /___ ___/ /
# \____/\____/_/  /_/_/  /_/\____/_/ |_/___/ /_/ /___/_____//____/


@app.get("/v1/communities")
def get_communities():
    pass
