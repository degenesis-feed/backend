import sqlite3


def get_connection():
    return sqlite3.connect("data.db")


def create_tables():
    con = get_connection()

    drop_following_table = """
        DROP TABLE IF EXISTS followings;
    """

    # DROP TABLE IF EXISTS comments;
    # DROP TABLE IF EXISTS reactions;

    create_following_table = """
        CREATE TABLE IF NOT EXISTS followings(
            following_id INTEGER PRIMARY KEY,
            user_address VARCHAR(255),
            following_address VARCHAR(255)
        );
    """

    with con:
        cursor = con.cursor()
        cursor.execute(drop_following_table)
        con.commit()
        cursor.execute(create_following_table)
        con.commit()
        cursor.close()


def add_mock_data():
    con = get_connection()
    mock_data_query = """
        INSERT INTO followings(user_address, following_address) VALUES
        ('test1', 'test2'), ('test1', 'test3');
    """
    with con:
        cursor = con.cursor()
        cursor.execute(mock_data_query)
        con.commit()
        cursor.close()


if __name__ == "__main__":
    print("Creating tables")
    create_tables()
    print("Tables created")
    add_mock_data()
