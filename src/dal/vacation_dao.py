from src.dal.database import jb_db_conn
import psycopg.sql 
import psycopg.rows as pgrows
from src.models.vacation_dto import VacationDto

class VacationDao:
    def __init__(self):
        self.table_name = "vacations"
    
    def get_all_vacations(self):
        with jb_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL("SELECT * FROM {};").format(psycopg.sql.Identifier(self.table_name)))
            result = cur.fetchall()
        print(result)
    
    def insert_into_vacations(self,vacation_dto):
         with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("INSERT INTO {} (country_id,vacation_description,arrival,departure,price,file_name) VALUES (%s,%s,%s,%s,%s,%s);").format(psycopg.sql.Identifier(self.table_name)),(vacation_dto.country_id,vacation_dto.vacation_description,vacation_dto.arrival,vacation_dto.departure,vacation_dto.price,vacation_dto.file_name))
            jb_db_conn.commit()

    def get_vacation_info_by_id(self,id):
        with jb_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL("SELECT * FROM {} WHERE id = %s;").format(psycopg.sql.Identifier(self.table_name)),(id,))
            result = cur.fetchall()
        print(result)
    
    def update_vacation_info_by_id(self,id,column,new_value):
        with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("UPDATE {} SET {} = %s WHERE id = %s;").format(psycopg.sql.Identifier(self.table_name),psycopg.sql.Identifier(column)),(new_value,id))
            jb_db_conn.commit()
    
    def delete_vacation_info_by_id(self,id):
        with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("DELETE FROM {} WHERE id = %s;").format(psycopg.sql.Identifier(self.table_name)),(id,))
            jb_db_conn.commit()
    
    def get_vacation_arrival_departure_time(self,arrival,departure):
        with jb_db_conn.cursor() as cur:
            cur.execute("SELECT arrival,departure FROM vacations WHERE arrival = %s and departure = %s;",(arrival,departure))
    
