# from tests.services.test_user_service import TestUserDao, TestUserService, TestInvalidUserService
# from tests.services.test_vacation_service import TestVacationDao,TestVacationService,TestInvalidVacationService
# from unittest import TestSuite,TextTestRunner
# import unittest
# def test_all():
#     test_cases = (TestVacationDao,TestVacationService,TestInvalidVacationService,TestUserDao,TestUserService,TestInvalidUserService)
    
#     suite = TestSuite()
    
#     for test_class in test_cases:
#         tests = unittest.defaultTestLoader.loadTestsFromTestCase(test_class)
#         suite.addTest(tests)

#     text_runner = TextTestRunner(verbosity=2)
#     text_runner.run(suite)

# run_all_tests.py
from unittest import TestSuite, TextTestRunner, defaultTestLoader

# import טסטי ה־services
from tests.services.test_user_service import (
    TestUserDao,
    TestUserService,
    TestInvalidUserService
)
from tests.services.test_vacation_service import (
    TestVacationDao,
    TestVacationService,
    TestInvalidVacationService
)

from tests.routes.test_auth_route import (
    TestJson,
    TestHtml,
    TestNegativeAuthHtml,
    TestNegativeAuthJson,

)

from tests.routes.test_vacation_route import (
    TestVacationHtml,
    TestVacationJson,
    TestNegativeVacationsHtml
)

def test_all():
    test_cases = [
        # services
        TestVacationDao,
        TestVacationService,
        TestInvalidVacationService,
        TestUserDao,
        TestUserService,
        TestInvalidUserService,
        # routes (frontend)
        TestJson,
        TestHtml,
        TestNegativeAuthHtml,
        TestNegativeAuthJson,
        TestVacationHtml,
        TestVacationJson,
        TestNegativeVacationsHtml
    ]

    suite = TestSuite()
    for case in test_cases:
        suite.addTests(defaultTestLoader.loadTestsFromTestCase(case))

    runner = TextTestRunner(verbosity=2)
    runner.run(suite)

if __name__ == '__main__':
    test_all()
