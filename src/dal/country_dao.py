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
    
    def get_country_info_by_id(self,id):
        with jb_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL("SELECT * FROM {} WHERE id = %s;").format(psycopg.sql.Identifier(self.table_name)),(id,))
            result = cur.fetchall()
        print(result)

    def update_country_info_by_id(self,id,column,new_value):
        with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("UPDATE {} SET {} = %s WHERE id = %s;").format(psycopg.sql.Identifier(self.table_name),psycopg.sql.Identifier(column)),(new_value,id))
            jb_db_conn.commit()
    
    def delete_country_info_by_id(self,id):
        with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("DELETE FROM {} WHERE id = %s;").format(psycopg.sql.Identifier(self.table_name)),(id,))
            jb_db_conn.commit()