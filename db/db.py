from psycopg2.extras import RealDictCursor


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


def add_description(con, address: str, description: str):
    query = """
        INSERT INTO profiles(address, description) VALUES
        (%s, %s);
    """
    with con:
        cursor = con.cursor()
        cursor.execute(query, (address, description))
    pass


def get_description(address):
    pass


def add_reaction(tx_hash):
    pass


def get_reactions(tx_hash):
    pass


def get_abi(con, contract_address):
    query = """
        SELECT abi FROM abis WHERE contract_address = %s;
    """
    with con:
        cursor = con.cursor()
        cursor.execute(query, (contract_address,))
        results = cursor.fetchall()
        clean_results = []
        for result in results:
            return result[0]


def add_abi(con, contract_address, abi):
    query = """
        INSERT INTO abis(contract_address, abi) VALUES
        (%s, %s);
    """
    with con:
        cursor = con.cursor()
        cursor.execute(query, (contract_address, abi))


def add_tx(
    con,
    tx_hash: str,
    from_add: str,
    to_add: str,
    input: str,
    function: str,
    raw_values: str,
    timestamp: str,
):
    query = """
        INSERT INTO transactions(tx_hash, from_add, to_add, input, function, raw_values, timestamp) VALUES
        (%s, %s, %s, %s, %s, %s, %s);
    """
    with con:
        cursor = con.cursor()
        cursor.execute(
            query, (tx_hash, from_add, to_add, input, function, raw_values, timestamp)
        )
    pass


def get_tx_hash(con, tx_hash: str):
    query = """
        SELECT (input, function, raw_values, timestamp) FROM transactions WHERE tx_hash = %s;
    """
    with con:
        cursor = con.cursor()
        cursor.execute(query, (tx_hash,))
        results = cursor.fetchall()
        for result in results:
            return result[0]


def get_tx_sender(con, from_add: str):
    query = """
        SELECT * FROM transactions WHERE from_add = %s;
    """
    with con:
        with con.cursor(cursor_factory=RealDictCursor) as cursor:
            cursor.execute(query, (from_add,))
            results = cursor.fetchall()
            return results
            # clean_results = []
            # for result in results:
            # print("in db:")
            # print(results)
            #     clean_results.append(result[0])


def get_last_tx_timestamp_for_sender(con, from_add: str):
    query = """
        SELECT MAX(timestamp) AS highest_timestamp
        FROM transactions
        WHERE from_add = %s;
    """
    with con:
        cursor = con.cursor()
        cursor.execute(query, (from_add,))
        results = cursor.fetchall()
        for result in results:
            return result[0]
