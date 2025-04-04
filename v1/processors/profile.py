class Profile:
    def __init__(self):
        # Default initialization (empty state until new is called)
        self.address = None
        self.is_signed_up = False
        self.description = None
        self.followers = []
        self.following = []
        self.transactions = []

    # Function for creating a new profile
    def new(self, address: str, description: str):
        # Add address as a string
        self.address = address

        # Have the is_signed_up status as true
        self.is_signed_up = True

        # Adding a little description if the user wanted that
        self.description = description

        # Create an empty array for followers for the user
        self.followers = []

        # Create an empty array for profiles the user follows
        self.following = []

    # Follow function for a profile
    def follow(self, who_to_follow: str) -> bool:
        # Fetch the profile object of who to follow
        profile = profile_of(who_to_follow)

        # Append the following user to the other users followers
        if self not in profile.followers:
            profile.followers.append(self)
        else:
            return False

        # Append the other user to profiles the following user follows
        if profile not in self.following:
            self.following.append(profile)
        else:
            return False

        return True

    def unfollow(self, who_to_unfollow: str) -> bool:
        profile = profile_of(who_to_unfollow)

        if self in profile.followers:
            profile.followers.remove(self)
        else:
            return False

        if profile in self.following:
            self.following.remove(profile)
        else:
            return False
        
        return True
    
    def get_actions(self);
        pass

def profile_of(address: str) -> Profile:
    # Getting the profile of a user based on address from database
    pass