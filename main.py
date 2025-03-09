from datetime import datetime
from src.dal.vacation_dao import VacationDao
from src.services import vacation_service
from src.models.vacation_dto import VacationDto
from src.dal.user_dao import UserDao
from src.services import user_service
from src.models.user_dto import UserDto
from src.models.likes_dto import LikesDto
from tests.test_user_service import TestUserService
from tests.test_user_service import TestInvalidUserService
from tests.test_user_service import TestUserDao, TestUserService, TestInvalidUserService
from tests.test_vacation_service import TestVacationDao,TestVacationService,TestInvalidVacationService
import unittest

if __name__ == '__main__':
    test_suite = unittest.TestSuite()
    loader = unittest.TestLoader()
    # הוספת הטסטים מכל המחלקות
    test_suite.addTest(loader.loadTestsFromTestCase(TestVacationDao))
    test_suite.addTest(loader.loadTestsFromTestCase(TestVacationService))
    test_suite.addTest(loader.loadTestsFromTestCase(TestInvalidVacationService))
    test_suite.addTest(loader.loadTestsFromTestCase(TestUserDao))
    test_suite.addTest(loader.loadTestsFromTestCase(TestUserService))
    test_suite.addTest(loader.loadTestsFromTestCase(TestInvalidUserService))

    
    runner = unittest.TextTestRunner(verbosity=2)
    runner.run(test_suite)






