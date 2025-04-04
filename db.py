import sqlite3
# from db_setup import get_connection


def get_followings(con, address: str):
    query = """
        SELECT following_address FROM followings WHERE user_address = ?;
    """
    with con:
        cursor = con.cursor()
        cursor.execute(query, (address,))
        results = cursor.fetchall()
        clean_results = []
        for result in results:
            clean_results.append(result[0])
        return clean_results
