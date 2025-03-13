from tests.test_user_service import TestUserDao, TestUserService, TestInvalidUserService
from tests.test_vacation_service import TestVacationDao,TestVacationService,TestInvalidVacationService
from unittest import TestSuite,TextTestRunner
import unittest
def test_all():
    test_cases = (TestVacationDao,TestVacationService,TestInvalidVacationService,TestUserDao,TestUserService,TestInvalidUserService)
    
    suite = TestSuite()
    
    for test_class in test_cases:
        tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
        suite.addTest(tests)

    text_runner = TextTestRunner(verbosity=2)
    text_runner.run(suite)