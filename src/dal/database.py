import psycopg as pg

from src.config import conn_info

test_db_conn = pg.connect(conninfo=conn_info)

