def get_followings(con, address: str):
    query = """
        SELECT following_address FROM followings WHERE user_address = %s;
    """
    with con:
        cursor = con.cursor()
        cursor.execute(query, (address,))
        results = cursor.fetchall()
        clean_results = []
        for result in results:
            clean_results.append(result[0])
        return clean_results


def get_followers(con, address: str):
    query = """
        SELECT user_address FROM followings WHERE following_address = %s;
    """
    # response = con.table("followings").select("user_address").execute()
    with con:
        cursor = con.cursor()
        cursor.execute(query, (address,))
        results = cursor.fetchall()
        clean_results = []
        for result in results:
            clean_results.append(result[0])
        return clean_results
    # return response


def add_following(con, user_address: str, following_address: str):
    query = """
        INSERT INTO followings(user_address, following_address) VALUES
        (%s, %s);
    """
    with con:
        cursor = con.cursor()
        cursor.execute(query, (user_address, following_address))
    pass


def add_comment():
    pass


def get_comments(tx_hash):
    pass


def add_description():
    pass


def get_description(address):
    pass


def add_reaction(tx_hash):
    pass


def get_reactions(tx_hash):
    pass
