from src.dal.vacation_dao import VacationDao
from src.models.vacation_dto import VacationDto
from src.dal.database import test_db_conn
import psycopg.sql
from typing import List, Optional


class VacationService:
    def __init__(self, vacation_dao: Optional[VacationDao] = None) -> None:
        """
        Initializes the vacation service with the provided VacationDao instance.

        :param vacation_dao: VacationDao instance used for vacation-related database operations
        """
        self.vacation_dao = vacation_dao or VacationDao()

    def get_all_vacations_by_order(self, order_by_column: str = "price") -> List[tuple]:
        """
        Retrieves all vacations from the database, ordered by the specified column.

        :param order_by_column: The column to order the results by (default is "price")
        :return: A list of tuples representing vacation data
        """
        with test_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL(
                "SELECT * FROM vacations ORDER BY {} ASC;").format(psycopg.sql.Identifier(order_by_column)))
            result = cur.fetchall()
        return result

    def validate_insert_of_new_vacation(self, vacation_dto: VacationDto) -> None:
        """
        Validates the vacation data before inserting a new vacation.

        :param vacation_dto: VacationDto object containing the vacation data
        :raises ValueError: If any of the validation checks fail (e.g., price, date)
        """
        if not isinstance(vacation_dto, VacationDto):
            raise ValueError("You must enter all of the fields to insert new vacation")

        if vacation_dto.price < 0 or vacation_dto.price > 10000:
            raise ValueError("Price cannot be negative or more than 10000")

        if vacation_dto.arrival > vacation_dto.departure:
            raise ValueError("Arrival date cannot be later than departure date")

        if self.vacation_dao.get_vacation_arrival_departure_time(vacation_dto.arrival, vacation_dto.departure) is not None:
            raise ValueError("You can't enter an existing arrival, departure dates")

    def validate_update_of_new_vacation(self, vacation_dto: VacationDto, column: str, new_value: str) -> None:
        """
        Validates the vacation data before updating a specific column of an existing vacation.

        :param vacation_dto: VacationDto object containing the current vacation data
        :param column: The column to update (e.g., "price", "arrival", "departure")
        :param new_value: The new value to set for the column
        :raises ValueError: If the update value does not meet the validation criteria
        """
        if column == "price":
            if new_value < 0 or new_value > 10000:
                raise ValueError("Price cannot be negative or more than 10000")

        elif column == "arrival":
            if new_value > vacation_dto.departure:
                raise ValueError("Arrival date cannot be later than departure date")
        
        elif column == "departure":
            if new_value < vacation_dto.arrival:
                raise ValueError("Departure date cannot be earlier than arrival date")

    def register_new_vacation(self, vacation_dto: VacationDto) -> None:
        """
        Registers a new vacation by inserting it into the database after validation.

        :param vacation_dto: VacationDto object containing the vacation data
        """
        self.validate_insert_of_new_vacation(vacation_dto)
        self.vacation_dao.insert_into_vacations(vacation_dto)

    def update_vacation_after_validation(self, id: int, column: str, new_value: str) -> None:
        """
        Updates an existing vacation's information after validating the new value.

        :param id: The ID of the vacation to update
        :param column: The column to update (e.g., "price", "arrival", "departure")
        :param new_value: The new value for the specified column
        :raises ValueError: If no vacation is found with the provided ID, or if validation fails
        """
        vacation_dto = self.vacation_dao.get_vacation_info_by_id(id)
        if vacation_dto is None:
            raise ValueError(f"No vacation found with ID {id}")
        self.validate_update_of_new_vacation(vacation_dto, column, new_value)
        self.vacation_dao.update_vacation_info_by_id(id, column, new_value)

    def delete_vacation_and_likes(self, id: int) -> None:
        """
        Deletes a vacation and its associated likes from the database.

        :param id: The ID of the vacation to delete
        """
        self.vacation_dao.delete_vacation_info_by_id(id)























# from src.dal.vacation_dao import VacationDao
# from src.models.vacation_dto import VacationDto
# from src.dal.database import test_db_conn
# import psycopg.sql


# class VacationService:
#     def __init__(self, vacation_dao: VacationDao):
#         self.vacation_dao = vacation_dao or VacationDao()

#     def get_all_vacations_by_order(self, order_by_column: str ="price"):
#         with test_db_conn.cursor() as cur:
#             cur.execute(psycopg.sql.SQL(
#                 "SELECT * FROM vacations ORDER BY {} ASC;").format(psycopg.sql.Identifier(order_by_column)))
#             result = cur.fetchall()
#         return result

#     def validate_insert_of_new_vacation(self, vacation_dto: VacationDto):
#         if not isinstance(vacation_dto, VacationDto):
#             raise ValueError(
#                 "You must enter all of the fields to insert new vacation")

#         if vacation_dto.price < 0 or vacation_dto.price > 10000:
#             raise ValueError("Price cannot be negative or more then 10000")

#         if vacation_dto.arrival > vacation_dto.departure:
#             raise ValueError(
#                 "arrival date cannot be later then departure date")

#         if self.vacation_dao.get_vacation_arrival_departure_time(vacation_dto.arrival, vacation_dto.departure):
#             raise ValueError(
#                 "You cant enter an existing arrival,departures dates")

#     def validate_update_of_new_vacation(self, vacation_dto,column,new_value):
#         if column == "price":
#             if new_value < 0 or new_value > 10000:
#                 raise ValueError("Price cannot be negative or more than 10000")

#         elif column == "arrival":
#             if new_value > vacation_dto.departure:
#                 raise ValueError("Arrival date cannot be later than departure date")
        
#         elif column == "departure":
#             if new_value < vacation_dto.arrival:
#                 raise ValueError("Departure date cannot be earlier than arrival date")
    
#     def register_new_vacation(self, vacation_dto):
#         self.validate_insert_of_new_vacation(vacation_dto)
#         self.vacation_dao.insert_into_vacations(vacation_dto)

#     def update_vacation_after_validation(self, id, column, new_value):
#         vacation_dto = self.vacation_dao.get_vacation_info_by_id(id)
#         if vacation_dto is None:
#             raise ValueError(f"No vacation found with ID {id}")
#         self.validate_update_of_new_vacation(vacation_dto,column,new_value)
#         self.vacation_dao.update_vacation_info_by_id(id, column, new_value)

#     def delete_vacation_and_likes(self, id):
#         self.vacation_dao.delete_vacation_info_by_id(id)
