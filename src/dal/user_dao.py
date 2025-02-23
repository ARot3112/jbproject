from src.dal.database import jb_db_conn
import psycopg.sql 
import psycopg.rows as pgrows
class UserDao:
    def __init__(self):
        self.table_name = "users"
    def get_all_users(self):
        with jb_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL("SELECT * FROM {};").format(psycopg.sql.Identifier(self.table_name)))
            result = cur.fetchall()
        print(result)
    
    def insert_into_users(self,first_name,last_name,email,password):
        with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("INSERT INTO {} (first_name,last_name,email,password) VALUES (%s,%s,%s,%s);").format(psycopg.sql.Identifier(self.table_name)),(first_name,last_name,email,password))
            jb_db_conn.commit()
    
    
    

