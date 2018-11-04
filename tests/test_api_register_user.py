import unittest
from flask import json, jsonify
from app import api
from db_helper import DBHelper
from models.users import User

class RegisterUserTestCase(unittest.TestCase):
    """
        contains tests for the REGISTER USER API ENDPOINT
    """
    def setUp(self):
        """sets up a new wsgi instance and a new post request to add a user"""
        self.client = api.test_client()
        self.db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        self.default_user = User("isnuwa@gmail.com", "Nuwagalb@1234", "attedndant")

    def test_for_invalid_email_address_on_login(self):
        """tests for an invalid email given on login"""
        login_response = self.client.post('api/v1/auth/login', content_type="application/json",
                            data=json.dumps({'email': 'admin100@storemanager.com', 'password': 'Admin@123'}))
        
        data = json.loads(login_response.data)

        self.assertEqual(
            data,
            {'error': 'Invalid email address. Please enter the correct email'})
        self.assertEqual(login_response.status_code, 401)

    def test_for_invalid_password_on_login(self):
        """tests for an invalid password given on login"""
        login_response = self.client.post('api/v1/auth/login', content_type="application/json",
                            data=json.dumps({'email': 'admin@storemanager.com', 'password': 'Admin@'}))
        
        data = json.loads(login_response.data)

        self.assertEqual(
            data,
            {'error': 'Invalid password. Please enter the correct password'})
        self.assertEqual(login_response.status_code, 401)

    def test_for_successfull_login(self):
        """tests for successful user login"""
        login_response = self.client.post('/api/v1/auth/login', content_type='application/json',
                        data=json.dumps({'email': 'admin@storemanager.com', 'password': 'Admin@123'}))

        login_data = json.loads(login_response.data)

        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(login_data['message'], 'admin@storemanager.com was successfully logged in')

    def test_store_attendant_is_successfully_created(self):
        """tests that an attendant is successfully created"""
        login_response = self.client.post('api/v1/auth/login', content_type="application/json",
                            data=json.dumps({"admin@storemanager.com", "Admin@123"}))
        
        data = json.loads(login_response.data)

        response = self.client.post('api/v1/auth/signup', content_type="application/json",
                        data=json.dumps({"attendant@storemanager.com", "Attendant1@123", "attendant"}))

        data = json.loads(response)
        self.assertEqual(
                data, 
                {"msg": "You  have successfully signed as joseph"})
        self.assertEqual(response.status_code, 201)

   