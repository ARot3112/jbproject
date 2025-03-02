from src.dal.vacation_dao import VacationDao
from src.models.vacation_dto import VacationDto
from src.dal.database import jb_db_conn
import psycopg.sql

class VacationService:
    def __init__(self,vacation_dao):
        self.vacation_dao = vacation_dao or VacationDao()
        
    def get_all_vacations_by_order(self,order_by_column="price"):
        with jb_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("SELECT * FROM vacations ORDER BY {} ASC;").format(psycopg.sql.Identifier(order_by_column)))
            result = cur.fetchall()
        return result
    
    def validate_insert_of_new_vacation(self,vacation_dto):
        if not isinstance(vacation_dto,VacationDto):
            raise ValueError("You must enter all of the fields to insert new vacation")
        
        if vacation_dto.price < 0 or vacation_dto.price > 10000:
            raise ValueError("Price cannot be negative or more then 10000")
        
        if vacation_dto.arrival > vacation_dto.departure:
            raise ValueError("arrival date cannot be later then departure date")
        
        if self.vacation_dao.get_vacation_arrival_departure_time(vacation_dto.arrival,vacation_dto.departure):
            raise ValueError("You cant enter an existing arrival,departures dates")
    
    def validate_update_of_new_vacation(self,vacation_dto):
        if not isinstance(vacation_dto,VacationDto):
            raise ValueError("You must enter all of the fields to insert new vacation")
        
        if vacation_dto.price < 0 or vacation_dto.price > 10000:
            raise ValueError("Price cannot be negative or more then 10000")
        
        if vacation_dto.arrival > vacation_dto.departure:
            raise ValueError("arrival date cannot be later then departure date")
        
    def insert_new_vacation_after_validation(self,vacation_dto):
        self.validate_insert_of_new_vacation(vacation_dto)
        self.vacation_dao.insert_into_vacations(vacation_dto)
       
        
    
    def update_vacation_after_validation(self,vacation_dto,id,column,new_value):
        self.validate_update_of_new_vacation(vacation_dto)
        self.vacation_dao.update_vacation_info_by_id(id,column,new_value)
    
    def delete_vacation_and_likes(self,id):
        self.vacation_dao.delete_vacation_info_by_id(id)
    



        
        
        

    
    

        
