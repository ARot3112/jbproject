from src.dal.database import db_conn
import psycopg.sql
import psycopg.rows as pgrows
from src.models.vacation_dto import VacationDto
from typing import List, Dict, Optional, Any


class VacationDao:
    def __init__(self) -> None:
        """
        Initializes the VacationDao class with the table name 'vacations'.
        """
        self.table_name: str = "vacations"

    def get_all_vacations(self) -> List[Dict[str, Any]]:
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            query = psycopg.sql.SQL(
                "SELECT {table}.*, countries.country_name AS country_name "
                "FROM {table} "
                "JOIN countries ON {table}.country_id = countries.id;"
            ).format(table=psycopg.sql.Identifier(self.table_name))

            cur.execute(query)
            result = cur.fetchall()
        return result

    def insert_into_vacations(self, vacation_dto: VacationDto) -> None:
        """
        Inserts a new vacation into the database.

        Args:
            vacation_dto (VacationDto): The vacation data transfer object containing vacation details.
        """
        with db_conn.cursor() as cur:
            cur.execute(
                psycopg.sql.SQL("INSERT INTO {} (country_id, vacation_description, arrival, departure, price, file_name) VALUES (%s, %s, %s, %s, %s, %s);").format(
                    psycopg.sql.Identifier(self.table_name)),
                (vacation_dto.country_id, vacation_dto.vacation_description, vacation_dto.arrival,
                 vacation_dto.departure, vacation_dto.price, vacation_dto.file_name)
            )
            db_conn.commit()
  

    def get_vacation_info_by_id(self, id: int) -> Optional[Dict[str, Any]]:
        """
        Retrieves vacation information by vacation ID.

        Args:
            id (int): The vacation ID.

        Returns:
            Optional[Dict[str, Any]]: A dictionary representing the vacation if found, otherwise None.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL(
                "SELECT * FROM {} WHERE id = %s;").format(psycopg.sql.Identifier(self.table_name)), (id,))
            result = cur.fetchone()
        return result

    def update_vacation_info_by_id(self, id: int, column: str, new_value: Any) -> None:
        """
        Updates vacation information by vacation ID.

        Args:
            id (int): The vacation ID.
            column (str): The column to update.
            new_value (Any): The new value to set.
        """
        with db_conn.cursor() as cur:
            cur.execute(
                psycopg.sql.SQL("UPDATE {} SET {} = %s WHERE id = %s;").format(
                    psycopg.sql.Identifier(
                        self.table_name), psycopg.sql.Identifier(column)
                ),
                (new_value, id)
            )
            db_conn.commit()

    def delete_vacation_info_by_id(self, id: int) -> None:
        """
        Deletes a vacation by vacation ID.

        Args:
            id (int): The vacation ID.
        """
        with db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("DELETE FROM {} WHERE id = %s;").format(
                psycopg.sql.Identifier(self.table_name)), (id,))
            db_conn.commit()

    def get_vacation_arrival_departure_time(self, arrival: str, departure: str) -> None:
        """
        Retrieves vacation arrival and departure times based on provided dates.

        Args:
            arrival (str): The arrival date.
            departure (str): The departure date.
        """
        with db_conn.cursor() as cur:
            cur.execute(
                "SELECT arrival, departure FROM vacations WHERE arrival = %s AND departure = %s;", (arrival, departure))
            result = cur.fetchone()
        return result
