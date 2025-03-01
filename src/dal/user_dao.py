from src.dal.database import jb_db_conn
import psycopg.sql 
import psycopg.rows as pgrows
from src.models.user_dto import UserDto


class UserDao:
    def __init__(self):
        self.table_name = "users"
    
    def get_all_users(self):
        with jb_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL("SELECT * FROM {};").format(psycopg.sql.Identifier(self.table_name)))
            result = cur.fetchall()
        print(result)
    
    def insert_into_users(self,user_dto):
        with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("INSERT INTO {} (first_name,last_name,email,password,role_id) VALUES (%s,%s,%s,%s,%s);").format(psycopg.sql.Identifier(self.table_name)),(user_dto.first_name,user_dto.last_name,user_dto.email,user_dto.password,user_dto.role_id))
            jb_db_conn.commit()
    
    def get_user_info_by_id(self,id):
        with jb_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL("SELECT * FROM {} WHERE id = %s;").format(psycopg.sql.Identifier(self.table_name)),(id,))
            result = cur.fetchall()
        print(result)
    
    def update_user_info_by_id(self,id,column,new_value):
        with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("UPDATE {} SET {} = %s WHERE id = %s;").format(psycopg.sql.Identifier(self.table_name),psycopg.sql.Identifier(column)),(new_value,id))
            jb_db_conn.commit()
    
    def delete_user_info_by_id(self,id):
        with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("DELETE FROM {} WHERE id = %s;").format(psycopg.sql.Identifier(self.table_name)),(id,))
            jb_db_conn.commit()
    
    def get_user_info_by_email_and_password(self,email,password):
        with jb_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL("SELECT * FROM users WHERE email = %s AND password = %s;"),(email,password))
            result = cur.fetchall()
        print(result)
    
    def check_if_email_exist(self,email):
        with jb_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL("SELECT email FROM USERS WHERE email = %s"),(email,))
            result = cur.fetchone()
        if result is not None:
            print(result)
    
