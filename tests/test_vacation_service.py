from src.models.vacation_dto import VacationDto
from src.dal.vacation_dao import VacationDao
from src.services.vacation_service import VacationService
import unittest
from src.dal.database import test_db_conn
import datetime
from typing import List, Tuple


class BaseTestVacationService(unittest.TestCase):
    """
    Base test class for Vacation Service tests. It sets up the database for testing by
    rolling back any previous transactions and clearing the `vacations` and `likes` tables.
    """
    
    def setUp(self) -> None:
        """
        Set up the test environment by rolling back any pending transactions
        and clearing the database tables for `vacations` and `likes`.
        """
        print(f"Running setup for {self.__class__.__name__}")
        test_db_conn.rollback()
        with test_db_conn.cursor() as cur:
            try:
                cur.execute("DELETE FROM vacations;")
                cur.execute("DELETE FROM likes;")
                test_db_conn.commit()
            except Exception as e:
                test_db_conn.rollback()
                print(f"Error during setup: {e}")
        self.vacation_dao = VacationDao()
        self.vacation_service = VacationService(self.vacation_dao)


class TestVacationDao(BaseTestVacationService):
    """
    Tests for the `VacationDao` class, which handles database operations related to vacations.
    """
    
    def setUp(self) -> None:
        """
        Set up the test environment for `VacationDao` tests.
        """
        super().setUp()

    def test_register_new_vacation(self) -> None:
        """
        Test the registration of a new vacation into the database I use it here because its used in the functions below.
        """
        vacation_dto = VacationDto(2, 'Amazing trip to Isr', datetime.date(2025, 12, 20), 
                                   datetime.date(2025, 12, 25), 3400, 'isr.jpg')
        self.vacation_service.register_new_vacation(vacation_dto)
        test_db_conn.commit()
        with test_db_conn.cursor() as cur:
            cur.execute(
                "SELECT country_id,vacation_description,arrival,departure,price,file_name FROM vacations WHERE price = %s;", 
                (vacation_dto.price,))
            print(type(vacation_dto.arrival))
            record = cur.fetchone()
        self.assertIsNotNone(record, "Expected a vacation_dto")
        self.assertEqual(record, (vacation_dto.country_id, vacation_dto.vacation_description, 
                                  vacation_dto.arrival, vacation_dto.departure, vacation_dto.price, vacation_dto.file_name), 
                         "Expected Equal values, Something went wrong")

    def test_invalid_register_new_vacation(self) -> None:
        """
        Test registering a new vacation with invalid dates (departure before arrival).
        """
        vacation_dto = VacationDto(2, 'Amazing trip to Isr', datetime.date(2025, 12, 20), 
                                   datetime.date(2025, 12, 13), 4200, 'isr.jpg')
        with self.assertRaises(ValueError):
            self.vacation_service.register_new_vacation(vacation_dto)


class TestVacationService(BaseTestVacationService):
    """
    Tests for the `VacationService` class, which handles the vacation business logic.
    """
    
    def setUp(self) -> None:
        """
        Set up the test environment for `VacationService` tests.
        """
        super().setUp()
        self.vacation_dto = VacationDto(2, 'Amazing trip to Isr', datetime.date(2025, 12, 20), 
                                        datetime.date(2025, 12, 25), 3400, 'isr.jpg')
        self.vacation_service.register_new_vacation(self.vacation_dto)
        test_db_conn.commit()
        with test_db_conn.cursor() as cur:
            cur.execute('SELECT id from vacations')
            self.vacation_id = cur.fetchone()[0]

    def test_get_all_vacations(self) -> None:
        """
        Test getting all vacations ordered by a specified column.
        """
        vacation_dto = VacationDto(3, 'Amazing trip to brazil', datetime.date(2025, 11, 20), 
                                   datetime.date(2025, 11, 25), 4000, 'brazil.jpg')
        self.vacation_service.register_new_vacation(vacation_dto)
        test_db_conn.commit()
        vacations = self.vacation_service.get_all_vacations_by_order(order_by_column="price")
        self.assertIsNotNone(vacations, 'Expected a list of vacations but got none')
        self.assertEqual(len(vacations), 2, 'Expected to get 2 vacations')
        self.assertEqual(vacations[0][5], self.vacation_dto.price, 
                         'Expected to get the lowest price from the vacations')

    def test_update_vacation(self) -> None:
        """
        Test updating a vacation's details.
        """
        self.vacation_service.update_vacation_after_validation(self.vacation_id, "price", 4000)
        test_db_conn.commit()
        with test_db_conn.cursor() as cur:
            cur.execute('SELECT price FROM vacations WHERE id = %s', (self.vacation_id,))
            record = cur.fetchone()
            self.assertIsNotNone(record, f"No record found for vacation ID {self.vacation_id}!")
            updated_price = record[0]
            self.assertEqual(updated_price, 4000, f'The new column is not equal to the {updated_price}')

    def test_delete_vacations_and_likes(self) -> None:
        """
        Test deleting a vacation and its associated likes from the database.
        """
        self.vacation_service.delete_vacation_and_likes(self.vacation_id)
        test_db_conn.commit()
        with test_db_conn.cursor() as cur:
            cur.execute('SELECT COUNT(*) from vacations')
            count = cur.fetchone()[0]
            self.assertEqual(count, 0, f"Expected 0 vacations, but found {count}!")
            cur.execute('SELECT COUNT(*) from likes WHERE vacation_id = %s', (self.vacation_id,))
            like_count = cur.fetchone()[0]
            self.assertEqual(like_count, 0, f"Expected 0 likes, but found {like_count}!")


class TestInvalidVacationService(BaseTestVacationService):
    """
    Tests for invalid operations within the `VacationService` class.
    """
    
    def setUp(self) -> None:
        """
        Set up the test environment for invalid operations in `VacationService` tests.
        """
        super().setUp()
        self.vacation_dto = VacationDto(2, 'Amazing trip to Isr', datetime.date(2025, 12, 20), 
                                        datetime.date(2025, 12, 25), 3400, 'isr.jpg')
        self.vacation_service.register_new_vacation(self.vacation_dto)
        test_db_conn.commit()
        with test_db_conn.cursor() as cur:
            cur.execute('SELECT id from vacations')
            self.vacation_id = cur.fetchone()[0]

    def test_invalid_update_vacation(self) -> None:
        """
        Test updating a vacation with invalid data (e.g., setting an unreasonable price).
        """
        with self.assertRaises(ValueError):
            self.vacation_service.update_vacation_after_validation(self.vacation_id, "price", 11000)
