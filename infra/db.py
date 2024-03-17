import os
from mysql import connector
from mysql.connector.connection import MySQLConnectionAbstract
from mysql.connector.pooling import PooledMySQLConnection


DB: MySQLConnectionAbstract | PooledMySQLConnection = None


def get_database():
    db_host = os.getenv("DB_HOST")
    db_port = int(os.getenv("DB_PORT"))
    db_user = os.getenv("DB_USER")
    db_pass = os.getenv("DB_PASS")
    db_name = os.getenv("DB_NAME")

    global DB
    if DB is None:
        DB = connector.connect(
            host=db_host,
            port=db_port,
            user=db_user,
            password=db_pass,
            database=db_name,
        )

    return DB


# import os
# import sqlalchemy
# from sqlalchemy.engine import Engine, Connection

# DB: Engine = None


# def get_database() -> Connection:
#     global DB
#     if DB is None:
#         DB = connect_tcp()
#     return DB.connect()


# def connect_tcp() -> Engine:
#     db_host = os.getenv("DB_HOST")
#     db_port = int(os.getenv("DB_PORT"))
#     db_user = os.getenv("DB_USER")
#     db_pass = os.getenv("DB_PASS")
#     db_name = os.getenv("DB_NAME")
#     connect_args = {}

#     url = sqlalchemy.engine.url.URL.create(
#         drivername="mysql",
#         username=db_user,
#         password=db_pass,
#         host=db_host,
#         port=db_port,
#         database=db_name,
#     )

#     return sqlalchemy.create_engine(
#         url,
#         connect_args=connect_args,
#         pool_size=20,
#         max_overflow=5,
#         pool_timeout=300,
#         pool_recycle=3600,
#     )
