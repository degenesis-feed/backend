from enum import Enum
from v1.utils.feedme_status import FeedMeStatus

class ProfileOrCommunity(Enum):
    PROFILE = "profile"
    COMMUNITY = "community"

    @classmethod
    def from_string(cls, value: str):
        """Convert a string to the corresponding ProfileOrCommunity enum value."""
        try:
            # Convert input to lowercase to make it case-insensitive
            value = value.lower()
            # Iterate through enum members to find a match
            for member in cls:
                if member.value == value:
                    return member
            raise FeedMeStatus.ERROR.create(f"No matching {cls.__name__} for string: {value}")
        except AttributeError:
            raise FeedMeStatus.ERROR.create(f"Input must be a string")