from src.dal.database import jb_db_conn
import psycopg.sql 
import psycopg.rows as pgrows
class VacationDao:
    def __init__(self):
        self.table_name = "vacations"
    def get_all_vacations(self):
        with jb_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL("SELECT * FROM {};").format(psycopg.sql.Identifier(self.table_name)))
            result = cur.fetchall()
        print(result)
    def insert_into_vacations(self,country_id,vacation_description,arrival,departure,price,file_name):
        with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("INSERT INTO {} (country_id,vacation_description,arrival,departure,price,file_name) VALUES (%s,%s,%s,%s,%s,%s);").format(psycopg.sql.Identifier(self.table_name)),(country_id,vacation_description,arrival,departure,price,file_name))
            jb_db_conn.commit()

