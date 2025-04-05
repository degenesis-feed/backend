import os
import psycopg2
from dotenv import load_dotenv

load_dotenv()

SERVER = os.getenv("PGHOST")
DATABASE_NAME = os.getenv("PGDATABASE")
USER = os.getenv("PGUSER")
PASSWORD = os.getenv("PGPASSWORD")
PORT = os.getenv("PGPORT")


def get_connection():
    return psycopg2.connect(
        dbname=DATABASE_NAME,
        user=USER,
        password=PASSWORD,
        host=SERVER,
        port=PORT,
    )


def drop_table(con, table_name: str):
    drop_query = f"""
        DROP TABLE IF EXISTS {table_name};
    """
    with con:
        cursor = con.cursor()
        cursor.execute(drop_query)
        con.commit()
        cursor.close()


def create_tables():
    con = get_connection()

    # DROP TABLE IF EXISTS comments;
    # DROP TABLE IF EXISTS reactions;

    create_following_table = """
        CREATE TABLE IF NOT EXISTS followings(
            following_id SERIAL PRIMARY KEY,
            user_address VARCHAR(255),
            following_address VARCHAR(255)
        );
    """

    create_transactions_table = """
        CREATE TABLE IF NOT EXISTS transactions(
            following_id SERIAL PRIMARY KEY,
            tx_hash VARCHAR(255),
            from_add VARCHAR(255),
            to_add VARCHAR(255),
            input TEXT,
            function TEXT,
            raw_values TEXT,
            timestamp BIGINT
        );
    """
    create_profiles_table = """
        CREATE TABLE IF NOT EXISTS profiles(
            profile_id SERIAL PRIMARY KEY,
            address VARCHAR(255),
            description TEXT
        );
    """

    create_description_table = """
        CREATE TABLE IF NOT EXISTS descriptions(
            description_id SERIAL PRIMARY KEY,
            description_text TEXT
        );
    """

    create_abi_table = """
        CREATE TABLE IF NOT EXISTS abis(
            abi_id SERIAL PRIMARY KEY,
            contract_address VARCHAR(255),
            abi TEXT
        );
    """

    with con:
        cursor = con.cursor()
        # cursor.execute(drop_following_table)
        # con.commit()
        # cursor.execute(create_following_table)
        # con.commit()
        # cursor.execute(create_profiles_table)
        # con.commit()
        # cursor.execute(create_abi_table)
        # con.commit()
        cursor.execute(create_transactions_table)
        con.commit()
        cursor.close()


def add_mock_data():
    con = get_connection()
    mock_data_query = """
        INSERT INTO followings(user_address, following_address) VALUES
        ('0xc0bffea543e5a701a2935a7aeae3e948587606b5', '0x4110eaa750f6f781a9bea2dd911ca5ba5b9a3e9d'),
        ('0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb', '0x993cd052b5f015e82a8fe8d5037f3afebf6bb928'),
        ('0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb', '0x0f4162c6148bed0dca1ff1a094708858a6d35723'),
        ('0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb', '0x79fad124e5bb17d56f50139a686c66481d287fd5'),
        ('0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb', '0x63629d63f648e253ee5d4bb0d93bb5473c8daf1e'),
        ('0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb', '0x912eb8d1ad5cdf730fd9eb5790f5b70d879013f3'),
        ('0x912eb8d1ad5cdf730fd9eb5790f5b70d879013f3', '0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb'),
        ('0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb', '0xdd7d37f72b6981f309525caa4403dd1e99eb65d5'),
        ('0xdd7d37f72b6981f309525caa4403dd1e99eb65d5', '0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb'),
        ('0x0f4162c6148bed0dca1ff1a094708858a6d35723', '0x7e0d5d54ad596c9ab6cfad4c6a9ae5d6f4651aeb');
    """
    with con:
        cursor = con.cursor()
        cursor.execute(mock_data_query)
        con.commit()
        cursor.close()


# if __name__ == "__main__":
#     print("Creating tables")
#     # create_tables()
#     print("Tables created")
#     # add_mock_data()
#     print("Mock data created")
