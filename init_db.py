import psycopg2
from db_config import connect

def create_tables():
    '''
    建表还得和产品battle，先确定细化需求
    :return:
    '''
    commands = [
        """
        CREATE TABLE IF NOT EXISTS users (
            user_id SERIAL PRIMARY KEY,
            username VARCHAR(50) UNIQUE NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS votes (
            vote_id SERIAL PRIMARY KEY,
            user_id INTEGER NOT NULL,
            option_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """,
        """
        CREATE TABLE IF NOT EXISTS options (
            option_id SERIAL PRIMARY KEY,
            option_text VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """
    ]
    try:
        conn = connect()
        cur = conn.cursor()
        for command in commands:
            cur.execute(command)
        conn.commit()
        cur.close()
        print("Tables created successfully.")
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

if __name__ == "__main__":
    create_tables()
