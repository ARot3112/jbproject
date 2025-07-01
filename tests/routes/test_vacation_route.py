import unittest
import os
from app import app
from src.dal.database import db_conn
from src.dal.vacation_dao import VacationDao
from src.models.vacation_dto import VacationDto
from src.services.vacation_service import VacationService
from src.dal.user_dao import UserDao
from src.models.user_dto import UserDto
from werkzeug.security import generate_password_hash
from uuid import uuid4

class BaseTestVacationRoute(unittest.TestCase):
    def setUp(self):
        os.environ['TESTING'] = 'True'
        self.app = app  
        self.app.config['TESTING'] = True        
        self.db_conn = db_conn
        self.client = self.app.test_client()
        self.vacation_dao = VacationDao()
        self.user_dao = UserDao()
        self.vacation_service = VacationService(self.vacation_dao)
        self.password = "test1"
        
        with self.db_conn.cursor() as cur:
            cur.execute("DELETE FROM vacations")
            cur.execute("DELETE FROM users WHERE email LIKE '%@a.com' OR email = 'superuser@example'")
            self.db_conn.commit()
        
        unique_email = f"user_{uuid4().hex[:10]}@a.com"
        self.user = {
            "email":  unique_email,
            "password": generate_password_hash(self.password),
            "role_id": 1,
            "first_name": "Test",
            "last_name": "User"
        }
        self.superuser = {
            "email": "superuser@example",
            "password": generate_password_hash(self.password),
            "role_id": 2,
            "first_name": "Super",
            "last_name": "User"
        }
        
        self.user_dao.insert_into_users(UserDto(**self.superuser))
        self.user_dao.insert_into_users(UserDto(**self.user))
        
        self.vacation = {
            "country_id": 1,
            "vacation_description": "Test vacation",
            "arrival": "2023-10-01",
            "departure": "2023-10-10",
            "price": 1000.0,
            "file_name": None
        }
        self.vacation_id = self.vacation_service.register_new_vacation(VacationDto(**self.vacation))
        self.db_conn.commit()
        
        with self.db_conn.cursor() as cur:
            cur.execute("SELECT id FROM vacations WHERE vacation_description = %s", ("Test vacation",))
            result = cur.fetchone()
            if result:
                self.vacation_id = result[0]
    
    def tearDown(self):
        with self.db_conn.cursor() as cur:
            cur.execute("DELETE FROM vacations WHERE vacation_description = %s", ("Test vacation",))
            cur.execute("DELETE FROM users WHERE email = %s", (self.user['email'],))
            cur.execute("DELETE FROM users WHERE email = %s", (self.superuser['email'],))
            self.db_conn.commit()

class TestVacationHtml(BaseTestVacationRoute):
    def test_list_vacations_page(self):
        self.client.post('/auth/login', data={
            'email': self.user['email'],
            'password': self.password,
        })
        response = self.client.get('/vacations/vacations_list')
        self.assertEqual(response.status_code, 200)

    def test_update_vacation_page(self):
        self.client.post('/auth/login', data={
            'email': self.superuser['email'],
            'password': self.password,
        })
        response = self.client.get(f'/vacations/update/{self.vacation_id}')
        self.assertEqual(response.status_code, 200)
    
    def test_create_vacation_page(self):
        self.client.post('/auth/login', data={
            'email': self.superuser['email'],
            'password': self.password,
        })
        response = self.client.get('/vacations/create')
        self.assertEqual(response.status_code, 200)
    
    def test_delete_vacation_page(self):
        self.client.post('/auth/login', data={
            'email': self.superuser['email'],
            'password': self.password,
        })
        response = self.client.get(f'/vacations/delete/{self.vacation_id}')
        self.assertEqual(response.status_code, 200)
    
    def test_like_vacation_page(self):
        self.client.post('/auth/login', data={
            'email': self.user['email'],
            'password': self.password,
        })
        response = self.client.get(f'/vacations/like/{self.vacation_id}')
        self.assertEqual(response.status_code, 302)

class TestVacationJson(BaseTestVacationRoute):
    def test_list_vacations_json(self):
        self.client.post('/api/auth/login', json={
            'email': self.user['email'],
            'password': self.password,
        })
        response = self.client.get('/api/vacations/vacations_list', headers={'Accept': 'application/json'})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_create_vacation_json(self):
        self.client.post('/api/auth/login', json={
            'email': self.superuser['email'],
            'password': self.password,
        })
        response = self.client.post('/api/vacations/create', 
            json={
                'country_id': 1,
                'vacation_description': 'New vacation',
                'arrival': '2023-11-01',
                'departure': '2023-11-10',
                'price': 1500.0
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.content_type, 'application/json')

    def test_update_vacation_json(self):
        self.client.post('/api/auth/login', json={
            'email': self.superuser['email'],
            'password': self.password,
        })
        response = self.client.put(f'/api/vacations/update/{self.vacation_id}', 
            json={
                'country_id': 1,
                'vacation_description': 'Updated vacation',
                'arrival': '2023-10-05',
                'departure': '2023-10-15',
                'price': 1200.0
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    def test_delete_vacation_json(self):
        self.client.post('/api/auth/login', json={
            'email': self.superuser['email'],
            'password': self.password,
        })
        response = self.client.delete(f'/api/vacations/delete/{self.vacation_id}', 
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')

    
    def test_like_vacation_json(self):
        self.client.post('/api/auth/login', json={
            'email': self.user['email'],
            'password': self.password,
        })
        response = self.client.post(f'/api/vacations/like/{self.vacation_id}', 
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
    
class TestNegativeVacationsHtml(BaseTestVacationRoute):
    def test_list_vacations_page_unauthenticated(self):
        response = self.client.get('/vacations/vacations_list')
        self.assertEqual(response.status_code, 401) 

    def test_update_vacation_page_unauthenticated(self):
        response = self.client.get(f'/vacations/update/{self.vacation_id}')
        self.assertEqual(response.status_code, 401)  
    def test_create_vacation_page_unauthenticated(self):
        response = self.client.get('/vacations/create')
        self.assertEqual(response.status_code, 401)  
    def test_delete_vacation_page_unauthenticated(self):
        response = self.client.get(f'/vacations/delete/{self.vacation_id}')
        self.assertEqual(response.status_code, 401)  
    def test_like_vacation_page_unauthenticated(self):
        response = self.client.get(f'/vacations/like/{self.vacation_id}')
        self.assertEqual(response.status_code, 401) 

class TestNegativeVacationsJson(BaseTestVacationRoute):
    def test_list_vacations_json_unauthenticated(self):
        response = self.client.get('/api/vacations/vacations_list', headers={'Accept': 'application/json'})
        self.assertEqual(response.status_code, 401) 

    def test_create_vacation_json_invalid_data(self):
        response = self.client.post('/api/vacations/create', 
            json={
                'country_id': 1,
                'vacation_description': 'New vacation',
                'arrival': '2023-11-01',
                'departure': '2023-11-10',
                'price': 11000.0
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)

    def test_update_vacation_json_invalid_vacation(self):
        response = self.client.put(f'/api/vacations/update/{self.vacation_id}', 
            json={
                'country_id': 14, 
                'vacation_description': 'Updated vacation',
                'arrival': '2023-10-05',
                'departure': '2023-10-15',
                'price': 1200.0
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)

    def test_delete_vacation_json_unauthenticated(self):
        response = self.client.delete(f'/api/vacations/delete/{self.vacation_id}', 
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 401)

    def test_like_vacation_json_unauthenticated(self):
        response = self.client.post(f'/api/vacations/like/{self.vacation_id}', 
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 401) 