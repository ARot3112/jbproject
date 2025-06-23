from src.dal.database import db_conn
import psycopg.sql
import psycopg.rows as pgrows

from typing import List, Dict, Optional


class LikesDao:
    def __init__(self) -> None:
        """
        Initializes the LikesDao class.
        Sets the table name to "likes".
        """
        self.table_name = "likes"

    def get_all_likes(self) -> List[Dict[str, Optional[str]]]:
        """
        Retrieves all records from the 'likes' table.

        Returns a list of dictionaries, where each dictionary represents a row in the table.

        Returns:
            List[Dict[str, Optional[str]]]: A list of dictionaries containing data for all rows in the 'likes' table.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL(
                "SELECT * FROM {};").format(psycopg.sql.Identifier(self.table_name)))
            result = cur.fetchall()
        return result

    def insert_into_likes(self, user_id: int, vacation_id: int) -> None:
        """
        Inserts a new record into the 'likes' table.

        Adds a record with the provided user_id and vacation_id to the table.

        Args:
            user_id (int): The user ID.
            vacation_id (int): The vacation ID.
        """
        with db_conn.cursor() as cur:
            cur.execute(
                psycopg.sql.SQL("INSERT INTO {} (user_id, vacation_id) VALUES (%s, %s);").format(
                    psycopg.sql.Identifier(self.table_name)),
                (user_id, vacation_id)
            )
            db_conn.commit()

    def get_likes_info_by_id(self, user_id: int, vacation_id: int) -> List[Dict[str, Optional[str]]]:
        """
        Retrieves the record from the 'likes' table for a specific user and vacation.

        Returns the record matching the provided user_id and vacation_id.

        Args:
            user_id (int): The user ID.
            vacation_id (int): The vacation ID.

        Returns:
            List[Dict[str, Optional[str]]]: A list of dictionaries representing the record matching the criteria.
        """
        with db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(
                psycopg.sql.SQL("SELECT * FROM {} WHERE user_id = %s AND vacation_id = %s;").format(
                    psycopg.sql.Identifier(self.table_name)),
                (user_id, vacation_id)
            )
            result = cur.fetchall()
        return result

    def delete_likes_info_by_id(self, user_id: int, vacation_id: int) -> None:
        """
        Deletes a record from the 'likes' table for a specific user and vacation.

        Deletes the record that matches the provided user_id and vacation_id.

        Args:
            user_id (int): The user ID.
            vacation_id (int): The vacation ID.
        """
        with db_conn.cursor() as cur:
            cur.execute(
                psycopg.sql.SQL("DELETE FROM {} WHERE user_id = %s AND vacation_id = %s;").format(
                    psycopg.sql.Identifier(self.table_name)),
                (user_id, vacation_id)
            )
            db_conn.commit()

    def get_likes_count(self, vacation_id: int) -> int:
        """
        Returns the number of likes for a vacation
        """
        with db_conn.cursor() as cur:
            cur.execute(
                psycopg.sql.SQL("SELECT COUNT(*) FROM {} WHERE vacation_id = %s;").format(
                    psycopg.sql.Identifier(self.table_name)),
                (vacation_id,)
            )
            result = cur.fetchone()
            return result[0] if result else 0
