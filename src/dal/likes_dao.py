from src.dal.database import jb_db_conn
import psycopg.sql 
import psycopg.rows as pgrows


class LikesDao:
    def __init__(self):
        self.table_name = "likes"
    
    def get_all_likes(self):
        with jb_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL("SELECT * FROM {};").format(psycopg.sql.Identifier(self.table_name)))
            result = cur.fetchall()
        print(result)
    
    def insert_into_likes(self,user_id,vacation_id):
        with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("INSERT INTO {} (user_id,vacation_id) VALUES (%s,%s);").format(psycopg.sql.Identifier(self.table_name)),(user_id,vacation_id))
            jb_db_conn.commit()
    
    
    def get_likes_info_by_id(self,user_id,vacation_id):
        with jb_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL("SELECT * FROM {} WHERE user_id = %s AND vacation_id = %s;").format(psycopg.sql.Identifier(self.table_name)),(user_id,vacation_id))
            result = cur.fetchall()
        print(result)
    

    def delete_likes_info_by_id(self,user_id,vacation_id):
        with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("DELETE FROM {} WHERE user_id = %s AND vacation_id = %s;").format(psycopg.sql.Identifier(self.table_name)),(user_id,vacation_id))
            jb_db_conn.commit()