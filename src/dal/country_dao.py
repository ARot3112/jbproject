from src.dal.database import jb_db_conn
import psycopg.sql 
import psycopg.rows as pgrows

class CountryDao:
    def __init__(self):
        self.table_name = "countries"
    def get_all_countries(self):
        with jb_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL("SELECT * FROM {};").format(psycopg.sql.Identifier(self.table_name)))
            result = cur.fetchall()
        print(result)
    def insert_into_countries(self,country_name):
        with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("INSERT INTO {} (country_name) VALUES (%s);").format(psycopg.sql.Identifier(self.table_name)),(country_name,))
            jb_db_conn.commit()