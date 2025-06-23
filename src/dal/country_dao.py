from src.dal.database import db_conn
import psycopg.sql
import psycopg.rows as pgrows
from typing import List, Dict, Optional


class CountryDao:
    def __init__(self) -> None:
        """
        Initializes the CountryDao class with the table name 'countries'.
        """
        self.table_name: str = "countries"

    def get_all_countries(self) -> List[Dict[str, any]]:
        """
        Retrieves all countries from the database.

        Returns:
            List[Dict[str, any]]: A list of dictionaries representing countries.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL(
                "SELECT * FROM {};").format(psycopg.sql.Identifier(self.table_name)))
            result = cur.fetchall()
        return result

    def insert_into_countries(self, country_name: str) -> None:
        """
        Inserts a new country into the database.

        Args:
            country_name (str): The name of the country to insert.
        """
        with db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("INSERT INTO {} (country_name) VALUES (%s);").format(
                psycopg.sql.Identifier(self.table_name)), (country_name,))
            db_conn.commit()

    def get_country_info_by_id(self, id: int) -> Optional[Dict[str, any]]:
        """
        Retrieves country information by country ID.

        Args:
            id (int): The country ID.

        Returns:
            Optional[Dict[str, any]]: A dictionary representing the country if found, otherwise None.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL(
                "SELECT * FROM {} WHERE id = %s;").format(psycopg.sql.Identifier(self.table_name)), (id,))
            result = cur.fetchone()
        return result

    def update_country_info_by_id(self, id: int, column: str, new_value: any) -> None:
        """
        Updates country information by country ID.

        Args:
            id (int): The country ID.
            column (str): The column to update.
            new_value (any): The new value to set.
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

    def delete_country_info_by_id(self, id: int) -> None:
        """
        Deletes a country by country ID.

        Args:
            id (int): The country ID.
        """
        with db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("DELETE FROM {} WHERE id = %s;").format(
                psycopg.sql.Identifier(self.table_name)), (id,))
            db_conn.commit()
