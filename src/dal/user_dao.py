from src.dal.database import test_db_conn
import psycopg.sql
import psycopg.rows as pgrows
from src.models.user_dto import UserDto
from typing import List, Dict, Optional, Any


class UserDao:
    def __init__(self) -> None:
        """
        Initializes the UserDao class with the table name 'users'.
        """
        self.table_name: str = "users"

    def get_all_users(self) -> List[Dict[str, Any]]:
        """
        Retrieves all users from the database.
        """
        with test_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL(
                "SELECT * FROM {};").format(psycopg.sql.Identifier(self.table_name)))
            result = cur.fetchall()
        return result

    def insert_into_users(self, user_dto: UserDto) -> None:
        """
        Inserts a new user into the database.

        Args:
            user_dto (UserDto): The user data transfer object containing user details.
        """
        with test_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("INSERT INTO {} (first_name, last_name, email, password, role_id) VALUES (%s, %s, %s, %s, %s);").format(
                psycopg.sql.Identifier(self.table_name)), (user_dto.first_name, user_dto.last_name, user_dto.email, user_dto.password, user_dto.role_id))
            test_db_conn.commit()

    def get_user_info_by_id(self, id: int) -> List[Dict[str, Any]]:
        """
        Retrieves user information by user ID.

        Args:
            id (int): The user ID.
        """
        with test_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL(
                "SELECT * FROM {} WHERE id = %s;").format(psycopg.sql.Identifier(self.table_name)), (id,))
            result = cur.fetchall()
        return result

    def update_user_info_by_id(self, id: int, column: str, new_value: Any) -> None:
        """
        Updates user information by user ID.

        Args:
            id (int): The user ID.
            column (str): The column to update.
            new_value (str): The new value to set.
        """
        with test_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("UPDATE {} SET {} = %s WHERE id = %s;").format(
                psycopg.sql.Identifier(self.table_name), psycopg.sql.Identifier(column)), (new_value, id))
            test_db_conn.commit()

    def delete_user_info_by_id(self, id: int) -> None:
        """
        Deletes a user by user ID.

        Args:
            id (int): The user ID.
        """
        with test_db_conn.cursor() as cur:
            cur.execute(psycopg.sql.SQL("DELETE FROM {} WHERE id = %s;").format(
                psycopg.sql.Identifier(self.table_name)), (id,))
            test_db_conn.commit()

    def get_user_info_by_email_and_password(self, email: str, password: str) -> List[Dict[str, Any]]:
        """
        Retrieves user information by email and password.

        Args:
            email (str): The user's email.
            password (str): The user's password.
        """
        with test_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL(
                "SELECT * FROM users WHERE email = %s AND password = %s;"), (email, password))
            result = cur.fetchall()
        return result

    def check_if_email_exist(self, email: str) -> Optional[Dict[str, Any]]:
        """
        Checks if an email exists in the database.

        Args:
            email (str): The email to check.
        """
        with test_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
            cur.execute(psycopg.sql.SQL(
                "SELECT email FROM USERS WHERE email = %s"), (email,))
            result = cur.fetchone()
        if result is not None:
            return result
        return None





















# from src.dal.database import test_db_conn
# import psycopg.sql
# import psycopg.rows as pgrows
# from src.models.user_dto import UserDto
# from typing import List, Dict, Optional


# class UserDao:
#     def __init__(self):
#         """
#         Initializes the UserDao class with the table name 'users'.
#         """
#         self.table_name: str = "users"

#     def get_all_users(self) -> List[Dict[str, any]]:
#         """
#         Retrieves all users from the database.
#         """
#         with test_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
#             cur.execute(psycopg.sql.SQL(
#                 "SELECT * FROM {};").format(psycopg.sql.Identifier(self.table_name)))
#             result = cur.fetchall()
#         return result

#     def insert_into_users(self, user_dto: UserDto):
#         """
#         Inserts a new user into the database.

#         Args:
#             user_dto (UserDto): The user data transfer object containing user details.
#         """
#         with test_db_conn.cursor() as cur:
#             cur.execute(psycopg.sql.SQL("INSERT INTO {} (first_name, last_name, email, password, role_id) VALUES (%s, %s, %s, %s, %s);").format(
#                 psycopg.sql.Identifier(self.table_name)), (user_dto.first_name, user_dto.last_name, user_dto.email, user_dto.password, user_dto.role_id))
#             test_db_conn.commit()

#     def get_user_info_by_id(self, id: int):
#         """
#         Retrieves user information by user ID.

#         Args:
#             id (int): The user ID.
#         """
#         with test_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
#             cur.execute(psycopg.sql.SQL(
#                 "SELECT * FROM {} WHERE id = %s;").format(psycopg.sql.Identifier(self.table_name)), (id,))
#             result = cur.fetchall()
#         return result

#     def update_user_info_by_id(self, id: int, column: str, new_value: any):
#         """
#         Updates user information by user ID.

#         Args:
#             id (int): The user ID.
#             column (str): The column to update.
#             new_value (str): The new value to set.
#         """
#         with test_db_conn.cursor() as cur:
#             cur.execute(psycopg.sql.SQL("UPDATE {} SET {} = %s WHERE id = %s;").format(
#                 psycopg.sql.Identifier(self.table_name), psycopg.sql.Identifier(column)), (new_value, id))
#             test_db_conn.commit()

#     def delete_user_info_by_id(self, id: int):
#         """
#         Deletes a user by user ID.

#         Args:
#             id (int): The user ID.
#         """
#         with test_db_conn.cursor() as cur:
#             cur.execute(psycopg.sql.SQL("DELETE FROM {} WHERE id = %s;").format(
#                 psycopg.sql.Identifier(self.table_name)), (id,))
#             test_db_conn.commit()

#     def get_user_info_by_email_and_password(self, email: str, password: str):
#         """
#         Retrieves user information by email and password.

#         Args:
#             email (str): The user's email.
#             password (str): The user's password.
#         """
#         with test_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
#             cur.execute(psycopg.sql.SQL(
#                 "SELECT * FROM users WHERE email = %s AND password = %s;"), (email, password))
#             result = cur.fetchall()
#         return result

#     def check_if_email_exist(self, email: str):
#         """
#         Checks if an email exists in the database.

#         Args:
#             email (str): The email to check.
#         """
#         with test_db_conn.cursor(row_factory=pgrows.dict_row) as cur:
#             cur.execute(psycopg.sql.SQL(
#                 "SELECT email FROM USERS WHERE email = %s"), (email,))
#             result = cur.fetchone()
#         if result is not None:
#             return result
