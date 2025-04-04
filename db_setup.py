import sqlite3


def get_connection():
    return sqlite3.connect("data.db")


def create_tables():
    con = get_connection()
    create_following_table = """
        CREATE TABLE IF NOT EXISTS followings(
            following_id SERIAL PRIMARY KEY,
            user_address VARCHAR(255),
            follwing_address VARCHAR(255)
        );
    """

    with con:
        cursor = con.cursor()
        cursor.execute(create_following_table)
        con.commit()
        cursor.close()


if __name__ == "__main__":
    print("Creating tables")
    create_tables()
    print("Tables created")
