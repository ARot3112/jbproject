import unittest
import os
from app import app
from src.dal.database import db_conn
from src.dal.user_dao import UserDao
from src.models.user_dto import UserDto
from werkzeug.security import generate_password_hash
from uuid import uuid4

class BaseTestAuthRoute(unittest.TestCase):
    def setUp(self):
        os.environ['TESTING'] = 'True'
        self.app = app  
        self.app.config['TESTING'] = True        
        self.db_conn = db_conn
        self.client = self.app.test_client()
        self.user_dao = UserDao()
        
       
        self.test_password = "test1"
        
        self.user ={
            "email":"test@example.com", 
            "password":generate_password_hash(self.test_password), 
            "role_id":1, 
            "first_name":"test", 
            "last_name":"test"}
        
        self.user_dao.insert_into_users(UserDto(**self.user))
    
    def tearDown(self):
        with self.db_conn.cursor() as cur:
            cur.execute("DELETE FROM users WHERE email = %s", ("test@example.com",))
            cur.execute("DELETE FROM users WHERE email LIKE %s", ("user_%@example.com",))
            self.db_conn.commit()


class TestHtml(BaseTestAuthRoute):
    def test_login_page(self):
        response = self.client.get('/auth/login')  
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Log In', response.data)
    
    def test_register_page(self):
        response = self.client.get('/auth/signup')  
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Create your account', response.data)
    
    def test_logout_page(self):
        self.client.post('/auth/login', data={
            'email': self.user['email'],
            'password': self.test_password
        })

        response = self.client.get('/auth/logout', headers={'Accept': 'text/html'})
        self.assertEqual(response.status_code, 302)

class TestJson(BaseTestAuthRoute):
    def test_login_json(self):
        response = self.client.post('/auth/login', 
            json={
                'email': self.user['email'], 
                'password': self.test_password  
            },
            content_type='application/json',
            follow_redirects=False
        )
        
        self.assertEqual(response.status_code, 200)
        
        self.assertEqual(response.content_type, 'application/json')
        
        data = response.get_json()
        
        self.assertIn('user', data)  
        self.assertEqual(data['user']['email'], self.user['email'])
        self.assertEqual(data['user']['role_id'], self.user['role_id'])
        

    def test_register_json(self):
        unique_email = f"testuser{uuid4().hex[:8]}@example.com"

        response = self.client.post('/auth/signup',
            json={
                'first_name': 'New',
                'last_name': 'User',
                'email': unique_email,
                'password': '123456'
            },
            headers={'Accept': 'application/json'},
            content_type='application/json'
        )
        self.assertIn(response.status_code, [200, 201], 
                     f"Expected 200 or 201, got {response.status_code}")
        
        self.assertIn('application/json', response.content_type or '')
        
        data = response.get_json()
        self.assertIsNotNone(data, "Response should contain JSON data")

    def test_logout_json(self):
        response = self.client.post('/auth/login', 
            json={
                'email': self.user['email'], 
                'password': self.test_password  
            },
            content_type='application/json',
            follow_redirects=False
        )
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.content_type, 'application/json')
        logout_response = self.client.get('/auth/logout', headers={'Accept': 'application/json'})
        self.assertEqual(logout_response.status_code, 200)
        self.assertEqual(logout_response.content_type, 'application/json')

        data = logout_response.get_json()
        self.assertIn('message', data)
        self.assertEqual(data['message'], 'Logged out successfully')


class TestNegativeHtml(BaseTestAuthRoute):
    def test_login_invalid_credentials(self):
        response = self.client.post('/auth/login', 
            data={
                'email': 'invalid_email',
                'password': 'invalid_password'
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'User not found', response.data)
    def test_register_invalid_data(self):
        response = self.client.post('/auth/signup',
            data={
                'first_name': '',
                'last_name': '',
                'email': 'invalid_email',
                'password': ''
            },
            follow_redirects=True
        )
        self.assertEqual(response.status_code, 400)
        self.assertIn(b'All fields are required.', response.data)
    def test_logout_without_login(self):
        response = self.client.get('/auth/logout', headers={'Accept': 'application/json'})
        self.assertEqual(response.status_code, 401)
        self.assertIn(b'Unauthorized access', response.data)
