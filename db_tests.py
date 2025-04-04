from db_setup import get_connection
from db import get_followers, get_followings

con = get_connection()

print("followings:")
print(get_followings(con, "0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb"))

print("")
print("followers")
print(get_followers(con, "0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb"))
