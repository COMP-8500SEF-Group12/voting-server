from db_config import get_db_connection


def drop_tables():
    conn = get_db_connection()
    cur = conn.cursor()

    # 删除表格的顺序需要注意外键约束，先删除依赖表，再删除主表
    tables = [
        'VoteResults',
        'Votes',
        'OptionList',
        'VotingOptions',
        'Votings',
        'Users_log',
        'Users'
    ]

    for table in tables:
        cur.execute(f'DROP TABLE IF EXISTS {table} CASCADE')

    conn.commit()
    cur.close()
    conn.close()



def init_db():
    conn = get_db_connection()
    cur = conn.cursor()

    # 创建 Users 表
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            user_id VARCHAR PRIMARY KEY,
            user_nickname VARCHAR DEFAULT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            has_vote_permission BOOLEAN DEFAULT FALSE
        )
    ''')
    cur.execute('''
        INSERT INTO Users (user_id, has_vote_permission)
        VALUES
        ('s1360912', TRUE),
        ('s1368301', TRUE),
        ('s1368789', TRUE),
        ('s1365524', TRUE),
        ('s1369455', TRUE),
        ('s1356774', TRUE),
        ('s1365751', TRUE),
        ('s1351838', TRUE),
        ('s1371097', TRUE),
        ('s1373353', TRUE)
    ''')


    # 创建 Votings 表
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Votings (
            voting_id SERIAL PRIMARY KEY,
            voting_name VARCHAR NOT NULL,
            voting_description TEXT,
            voting_date DATE,
            status VARCHAR CHECK (status IN ('open', 'closed', 'pending')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            create_user_id VARCHAR NOT NULL,
            delete_status VARCHAR DEFAULT 'N'
        )
    ''')

    # 创建 VotingOptions 表
    cur.execute('''
        CREATE TABLE IF NOT EXISTS VotingOptions (
            option_id SERIAL PRIMARY KEY,
            voting_id INTEGER REFERENCES Votings(voting_id),
            option_title VARCHAR NOT NULL,
            option_type VARCHAR CHECK (option_type IN ('single', 'multi')),
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 创建 OptionList 表
    cur.execute('''
        CREATE TABLE IF NOT EXISTS OptionList (
            list_id SERIAL PRIMARY KEY,
            option_id INTEGER REFERENCES VotingOptions(option_id),
            list_title VARCHAR NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')


    # 创建 Votes 表
    cur.execute('''
        CREATE TABLE IF NOT EXISTS Votes (
            vote_id SERIAL PRIMARY KEY,
            user_id VARCHAR REFERENCES Users(user_id),
            voting_id INTEGER REFERENCES Votings(voting_id),
            option_id INTEGER REFERENCES VotingOptions(option_id),
            list_id INTEGER REFERENCES OptionList(list_id),
            is_voted BOOLEAN,
            vote_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    # 创建 VoteResults 表
    cur.execute('''
        CREATE TABLE IF NOT EXISTS VoteResults (
            result_id SERIAL PRIMARY KEY,
            voting_id INTEGER REFERENCES Votings(voting_id),
            option_id INTEGER REFERENCES VotingOptions(option_id),
            list_id INTEGER REFERENCES OptionList(list_id),
            vote_count INTEGER,
            list_percentage FLOAT,
            last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')

    conn.commit()
    cur.close()
    conn.close()



if __name__ == '__main__':
    drop_tables()
    print("All tables have been dropped successfully.")
    init_db()
    print("All tables have been inited successfully.")
