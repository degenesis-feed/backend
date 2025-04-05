class Community:
    def __init__(self, name: str, description: str):
        self.members = []
        self.roi = 0
        self.name = name
        self.description = description
        self.followers = []

    def add_profile(self, wallet: str):
        pass

    def remove_profile(self, wallet: str):
        pass

def get_community(name: str) -> Community:
    # con = get_connection()
    pass
