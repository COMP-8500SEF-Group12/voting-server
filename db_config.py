# PG版本 16
import pg8000

# 数据库连接参数
def get_db_connection():
    db_params = {
        'database': 'postgres',
        'user': 'postgres',
        'password': 'group12',
        'host': '134.209.107.254',
        'port': 5432
    }

    connection = pg8000.connect(**db_params)
    return connection

