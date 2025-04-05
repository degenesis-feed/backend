from v1.processors.nodit import Nodit
from db.db_setup import get_connection
from v1.utils.feedme_status import FeedMeStatus
from v1.processors.community import get_community
from v1.processors.web3wrapper import Web3wrapper
from v1.processors.curvegrid import make_contract_instance
from db.db import get_followers, get_followings, add_following, add_description

nodit = Nodit()
w3w = Web3wrapper()

class Profile:
    def __init__(self, address: str, followers: list = [], followings: list = []):
        # Default initialization (empty state until new is called)
        self.address = address
        self.is_signed_up = False
        self.description = None
        self.followers = followers
        self.following = followings
        self.community_followings = []
        self.actions = []

    # Function for creating a new profile
    def new(self, description: str) -> FeedMeStatus:
        # Have the is_signed_up status as true
        if self.is_signed_up:
            return FeedMeStatus.ERROR.create(f"User {self.address} already signed up")

        self.is_signed_up = True

        # Adding a little description if the user wanted that
        self.description = description

        # Create an empty array for followers for the user
        con = get_connection()
        self.followers = get_followers(con, self.address)
        add_description(con, self.address, description)

        # Create an empty array for profiles the user follows
        self.following = []

        # Create an empty array for communities that this user follows
        self.community_followings = []

        return FeedMeStatus.SUCCESS.create(
            f"Managed to sign up a new profile for {self.address}"
        )

    # Follow function for a profile
    def follow_profile(self, who_to_follow: str) -> FeedMeStatus:
        # Fetch the profile object of who to follow
        profile = profile_of(who_to_follow)

        # Append the following user to the other users followers
        if self.address not in profile.followers:
            profile.followers.append(self.address)
        else:
            return FeedMeStatus.ERROR.create(f"You already follow {profile.address}")

        # Append the other user to profiles the following user follows
        if profile.address not in self.following:
            self.following.append(profile.address)
        else:
            return FeedMeStatus.ERROR.create(
                f"{profile.address} already have you in its followers, contact admin"
            )

        # Update database
        con = get_connection()
        add_following(con, self.address, profile.address)

        # FUCKING SUCCESS 😎
        return FeedMeStatus.SUCCESS.create(
            f"Succeeded to follow profile: {profile.address}"
        )

    # Unfollow function for a wallet
    def unfollow_profile(self, who_to_unfollow: str) -> FeedMeStatus:
        # Fetch the profile of who the user wishes to unfollow
        profile = profile_of(who_to_unfollow)

        # Remove user from this profiles followers
        if self.address in profile.followers:
            profile.followers.remove(self.address)
        else:
            return FeedMeStatus.ERROR.create(
                f"You are not even following {profile.address}"
            )

        # Remove the profile from the users following list
        if profile.address in self.following:
            self.following.remove(profile.address)
        else:
            return FeedMeStatus.ERROR.create(
                f"{profile.address} doesn't have you as a follower, contact admin"
            )

        # FUCKING SUCCESS 😎
        return FeedMeStatus.SUCCESS.create(
            f"Succeeded to unfollow profile: {profile.address}"
        )

    # Function for following a community
    def follow_community(self, name_of_community: str) -> FeedMeStatus:
        # Fetch the community in question
        community = get_community(name_of_community)

        # Append community name to the communities that the address follows
        if community.name not in self.community_followings:
            self.community_followings.append(community.name)
        else:
            return FeedMeStatus.ERROR.create(f"You already follow {community.name}")

        # Append the address to followers of the community
        if self.address not in community.followers:
            community.followers.append(self.address)
        else:
            return FeedMeStatus.ERROR.create(
                f"{community.name} already have you as a follower, please contact admin"
            )

        # FUCKING SUCCESS 😎
        return FeedMeStatus.SUCCESS.create(
            f"Succeeded to follow community: {community}"
        )

    # Function for unfollowing a community
    def unfollow_community(self, name_of_community: str) -> FeedMeStatus:
        # Fetch the community in question
        community = get_community(name_of_community)

        # Remove the community name from the communities that the wallet follows
        if community.name in self.community_followings:
            self.community_followings.append(community.name)
        else:
            return FeedMeStatus.ERROR.create(f"You don't even follow {community.name}")

        # Remove the wallet address from followers of the community
        if self.address in community.followers:
            community.followers.append(self.address)
        else:
            return FeedMeStatus.ERROR.create(
                f"{community.name} doesn't have you as a follower, please contact admin"
            )

        # FUCKING SUCCESS 😎
        return FeedMeStatus.SUCCESS.create(
            f"Succeeded to unfollow community: {community}"
        )

    def get_actions(self) -> FeedMeStatus:
        return FeedMeStatus.SUCCESS.create(f"Actions of {self.address}", self.actions)

    def fill_actions(self) -> FeedMeStatus:
        for addy in self.following:
            # Also, should we have some caching here based on timestamp? Like fetching last timestamp of last tx that is potentially 
            # in the db, and then utelize this in the get_historical to save time?
            txs_rawish = nodit.get_historical(address=addy)
            for raw_tx in txs_rawish:
                contract_abi = make_contract_instance(raw_tx["to"])
                decoded_tx = w3w.parse_input(abi=contract_abi, encoded_input=raw_tx["input"], contract_address=raw_tx["to"])
                # Fill in here with database stuff to enter the decoded data for each tx
                # Suggesting maybe hash -> method name -> method arguments, as a dynamic typed array

def profile_of(address: str) -> Profile:
    con = get_connection()
    following = get_followings(con, address)
    followers = get_followers(con, address)
    # get profile description
    # Getting the profile of a user based on address from database
    profile = Profile(address=address, followers=followers, followings=following)
    return profile
