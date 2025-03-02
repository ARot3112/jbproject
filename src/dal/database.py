import psycopg as pg

from src.config import conn_info

jb_db_conn = pg.connect(conninfo=conn_info)
