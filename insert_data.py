from db_config import connect

def insert_option(option_text):
    '''
    示例，
    :param option_text:
    :return:
    '''
    sql = """INSERT INTO options(option_text) VALUES(%s) RETURNING option_id;"""
    conn = None
    option_id = None
    try:
        conn = connect()
        cur = conn.cursor()
        cur.execute(sql, (option_text,))
        option_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
    return option_id

def insert_vote(vote_text):
    pass

def insert_xxx():
    pass