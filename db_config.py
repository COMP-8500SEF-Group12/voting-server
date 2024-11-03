import psycopg2

# PG版本 17.0.1

def connect():
    return psycopg2.connect(
        host="localhost",
        database="voting_system",
        user="username",
        password="password"
    )

