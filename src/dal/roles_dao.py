from src.dal.database import test_db_conn
import psycopg.sql
import psycopg.rows as pgrows
import psycopg.sql
from typing import List, Dict, Any


class RolesDao:
    def __init__(self) -> None:
        """
        Initializes the RolesDao class with the table name 'roles'.
        """
        self.table_name = "roles"

    def get_all_roles(self) -> List[Dict[str, Any]]:
        """
        Retrieves all roles from the database.

        Returns:
            List[Dict[str, Any]]: A list of dictionaries containing role information.
        """
        with test_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL(
                "SELECT * FROM {};").format(psycopg.sql.Identifier(self.table_name)))
            result = cur.fetchall()
        return result

    def insert_into_roles(self, name: str) -> None:
        """
        Inserts a new role into the database.

        Args:
            name (str): The name of the role.
        """
        with test_db_conn.cursor() as cur:
            cur.execute(
                psycopg.sql.SQL("INSERT INTO {} (name) VALUES (%s);")
                .format(psycopg.sql.Identifier(self.table_name)), (name,)
            )
            test_db_conn.commit()

    def get_roles_info_by_id(self, id: int) -> List[Dict[str, Any]]:
        """
        Retrieves role information by role ID.

        Args:
            id (int): The role ID.

        Returns:
            List[Dict[str, Any]]: A list containing role details.
        """
        with test_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(
                psycopg.sql.SQL("SELECT * FROM {} WHERE id = %s;")
                .format(psycopg.sql.Identifier(self.table_name)), (id,)
            )
            result = cur.fetchall()
        return result

    def update_roles_info_by_id(self, id: int, column: str, new_value: Any) -> None:
        """
        Updates role information by role ID.

        Args:
            id (int): The role ID.
            column (str): The column to update.
            new_value (Any): The new value to set.
        """
        with test_db_conn.cursor() as cur:
            cur.execute(
                psycopg.sql.SQL("UPDATE {} SET {} = %s WHERE id = %s;")
                .format(psycopg.sql.Identifier(self.table_name), psycopg.sql.Identifier(column)),
                (new_value, id),
            )
            test_db_conn.commit()

    def delete_roles_info_by_id(self, id: int) -> None:
        """
        Deletes a role by role ID.

        Args:
            id (int): The role ID.
        """
        with test_db_conn.cursor() as cur:
            cur.execute(
                psycopg.sql.SQL("DELETE FROM {} WHERE id = %s;")
                .format(psycopg.sql.Identifier(self.table_name)), (id,)
            )
            test_db_conn.commit()

