from src.models.user_dto import UserDto
from src.services.user_service import UserServices
import unittest
from src.dal.database import db_conn
from src.models.likes_dto import LikesDto
from typing import Optional


class BaseTestUserService(unittest.TestCase):
    """
    Base test class for User Service tests. It sets up the database for testing by
    rolling back any previous transactions and clearing the `users` and `likes` tables.
    """

    def setUp(self) -> None:
        """
        Set up the test environment by rolling back any pending transactions
        and clearing the database tables for `users` and `likes`.
        It also ensures there is at least one vacation in the database.
        """
        print(f"Running setup for {self.__class__.__name__}")
        db_conn.rollback()
        with db_conn.cursor() as cur:
            try:
                cur.execute("DELETE FROM users;")
                cur.execute("DELETE FROM likes;")
                cur.execute("SELECT COUNT(*) FROM vacations;")
                count = cur.fetchone()[0]
                if count == 0:
                    cur.execute("INSERT INTO vacations (country_id, vacation_description, arrival, departure, price, file_name) VALUES (1, 'Test Vacation', '2025-12-20', '2025-12-25', 1000, 'test.jpg') RETURNING id;")
                    vacation_id = cur.fetchone()[0]
                else:
                    cur.execute("SELECT id FROM vacations LIMIT 1;")
                    vacation_id = cur.fetchone()[0]

                self.vacation_id = vacation_id
                db_conn.commit()

            except Exception as e:
                db_conn.rollback()
                print(f"Error during setup: {e}")

        self.user_service = UserServices()


class TestUserDao(BaseTestUserService):
    """
    Tests for the `UserDao` class, which handles database operations related to users.
    """

    def setUp(self) -> None:
        """
        Set up the test environment for `UserDao` tests, I use it in here separately because its used in the functions below.
        """
        super().setUp()

    def test_register_new_user(self) -> None:
        """
        Test the registration of a new user into the database.
        """
        user_dto = UserDto('Test', 'User', 'Example@gmail.com', 'password', 1)
        self.user_service.register_new_user(user_dto)
        db_conn.commit()

        with db_conn.cursor() as cur:
            cur.execute(
                "SELECT first_name, last_name, email, password, role_id FROM users WHERE email = %s;", (user_dto.email,))
            record = cur.fetchone()

        self.assertIsNotNone(record, "User was not inserted into the database")
        self.assertEqual(record, (user_dto.first_name, user_dto.last_name, user_dto.email, user_dto.password, user_dto.role_id),
                         "Inserted user data does not match expected values")

    def test_register_new_user_invalid_email(self) -> None:
        """
        Test registering a new user with an invalid email format.
        """
        user_dto = UserDto('Test', 'User', 'invalid@@gmail.c', 'password', 1)
        with self.assertRaises(ValueError):
            self.user_service.register_new_user(user_dto)


class TestUserService(BaseTestUserService):
    """
    Tests for the `UserService` class, which handles user-related business logic.
    """

    def setUp(self) -> None:
        """
        Set up the test environment for `UserService` tests by registering a new user.
        """
        super().setUp()
        self.user_dto = UserDto(
            'Test', 'User', 'Example@gmail.com', 'password', 1)
        self.user_service.register_new_user(self.user_dto)
        db_conn.commit()
        with db_conn.cursor() as cur:
            cur.execute('SELECT id from users;')
            self.user_id = cur.fetchone()[0]

    def test_like_a_vacation(self) -> None:
        """
        Test liking a vacation.
        """
        likes_dto = LikesDto(self.user_id, self.vacation_id)
        self.user_service.like_a_vacation(likes_dto)
        with db_conn.cursor() as cur:
            cur.execute("SELECT * FROM likes WHERE user_id = %s AND vacation_id = %s;",
                        (self.user_id, self.vacation_id))
            record = cur.fetchone()
            self.assertIsNotNone(record,
                                 f"Expected a like record for user_id={self.user_id} and vacation_id={self.vacation_id}")
            self.assertEqual(record, (self.user_id, self.vacation_id),
                             "The like record does not match expected values")

    def test_log_in_user(self) -> None:
        """
        Test logging in a user with correct credentials.
        """
        self.user_service.log_in_user(self.user_dto)
        with db_conn.cursor() as cur:
            cur.execute("SELECT email, password FROM users WHERE email = %s AND password = %s;",
                        (self.user_dto.email, self.user_dto.password))
            record = cur.fetchone()
            self.assertIsNotNone(record, "Expected an email and password")
            self.assertEqual(
                record, (self.user_dto.email, self.user_dto.password))

    def test_unlike_a_vacation(self) -> None:
        """
        Test unliking a vacation.
        """
        like_dto = LikesDto(self.user_id, self.vacation_id)
        self.user_service.like_a_vacation(like_dto)
        self.user_service.un_like_a_vacation(like_dto)
        with db_conn.cursor() as cur:
            cur.execute('SELECT * FROM likes WHERE user_id = %s;',
                        (self.user_id,))
            record = cur.fetchone()
            self.assertIsNone(
                record, 'The likes table should be empty after unliking')


class TestInvalidUserService(BaseTestUserService):
    """
    Tests for invalid operations within the `UserService` class.
    """

    def setUp(self) -> None:
        """
        Set up the test environment for invalid operations in `UserService` tests by registering a new user.
        """
        super().setUp()
        self.user_dto = UserDto(
            'Test', 'User', 'Example@gmail.com', 'password', 1)
        self.user_service.register_new_user(self.user_dto)
        with db_conn.cursor() as cur:
            cur.execute('SELECT id from users;')
            self.user_id = cur.fetchone()[0]

    def test_like_a_vacation_vacation_id_invalid(self) -> None:
        """
        Test liking a vacation with an invalid vacation ID.
        """
        likes_dto = LikesDto(self.user_id, '9999')
        with self.assertRaises(TypeError):
            self.user_service.like_a_vacation(likes_dto)

    def test_log_in_user_invalid_password(self) -> None:
        """
        Test logging in a user with an invalid password.
        """
        user_dto = UserDto('Test', 'User', 'Example@gmail.com', 'pas', 1)
        with self.assertRaises(ValueError):
            self.user_service.log_in_user(user_dto)

    def test_invalid_unlike_a_vacation(self) -> None:
        """
        Test unliking a vacation with invalid parameters.
        """
        like_dto = LikesDto('31', '99')
        with self.assertRaises(TypeError):
            self.user_service.un_like_a_vacation(like_dto)
