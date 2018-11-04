import unittest
from flask import json
from app import api
from db_helper import DBHelper
from models.users import User

class APIUserTestCase(unittest.TestCase):
    """
        contains tests for USER REGISTERATION AND LOGIN ENDPOINTS
    """
    def setUp(self):
        """sets up a new wsgi instance"""
        self.client = api.test_client()
        self.user_instance = User("admin@storemanager.com", "Admin@123", "admin")
        self.invalid_user_email = {'email': 'admin100@storemanager.com', 'password': 'Admin@123'}
        self.invalid_user_password = {'email': 'admin@storemanager.com', 'password': 'Admin@124'}
        self.valid_user_details = {'email': 'admin@storemanager.com', 'password': 'Admin@123'}
        self.sales_attendant = {'email': 'attendant@storemanager.com', 'password': 'Attendant@123'}
        self.missing_email_key = {'': 'admin100@storemanager.com', 'password': 'Admin@123'}
        self.missing_password_key = {'email': 'admin100@storemanager.com', '': 'Admin@123'}
        self.missing_email_value = {'email': None, 'password': 'Admin@123'}
        self.missing_password_value = {'email': 'admin100@storemanager.com', 'password': None}
        self.empty_string = {'email': "", 'password': 'Admin@123'}
        
        
        
    def tearDown(self):
        """creates and drops tables used in testing"""
        self.db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        self.db.drop_users_test_table()
        self.db.create_users_test_table()


    def test_for_invalid_email_address_on_login(self):
        """tests for an invalid email given on login"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.invalid_user_email))
        
        data = json.loads(login_response.data)

        self.assertEqual(login_response.status_code, 404)
        self.assertEqual(
            data['error'],
            'Invalid email address. Please enter the correct email'
        )

    def test_for_invalid_password_on_login(self):
        """tests for an invalid password given on login"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.invalid_user_password))
        
        data = json.loads(login_response.data)

        self.assertEqual(login_response.status_code, 404)
        self.assertEqual(
            data['error'],
            'Invalid password. Please enter the correct password')

    def test_for_successfull_login(self):
        """tests for successful user login"""
        login_response = self.client.post('/api/v2/auth/login', content_type='application/json',
                        data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)

        self.assertEqual(login_response.status_code, 200)
        self.assertEqual(
            login_data['message'],
            'admin@storemanager.com was successfully logged in'
        )

    def test_store_attendant_account_is_successfully_created(self):
        """tests that an attendant is successfully created"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']        
        
        reg_response = self.client.post('api/v2/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(reg_response.data)
        self.assertEqual(reg_response.status_code, 201)
        self.assertEqual(data['user_id'], 2)
        self.assertEqual(data['email'], 'attendant@storemanager.com')
        self.assertEqual(data['role'], 'attendant')

    def test_error_message_is_returned_on_duplicate_registration_of_an_attendant(self):
        """test for duplicate registration"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']        
        
        reg_response_one = self.client.post('api/v2/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        reg_response_two = self.client.post('api/v2/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(reg_response_two.data)
        self.assertEqual(reg_response_two.status_code, 409)
        self.assertEqual(
            data['error'],
            'Email address already exists. Please provide a different email'
        )

    def test_user_without_admin_rights_cannot_create_new_sales_attendants_account(self):
        """tests for unauthorized access of sinup method by the store attendant"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']        
        
        reg_response = self.client.post('api/v2/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_login = self.client.post('api/v2/auth/login', content_type="application/json",
                                    data=json.dumps(self.sales_attendant))

        attendant_data = json.loads(attendant_login.data)
        attendant_token = attendant_data['token'] 

        attendant_registration_attempt = self.client.post('api/v2/auth/signup', 
                                    content_type="application/json",
                                    data=json.dumps(self.sales_attendant),
                                    headers={'Authorization': 'Bearer {}'.format(attendant_token)})

        data = json.loads(attendant_registration_attempt.data)
        self.assertEqual(attendant_registration_attempt.status_code, 403)
        self.assertEqual(
            data['error'],
            'Access to this resource is forbidden'
        )

    def test_for_missing_email_key_on_attempt_to_login(self):
        """tests for a missing email key when user attempts to login"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.missing_email_key))
        data = json.loads(login_response.data)
        self.assertEqual(login_response.status_code, 400)
        self.assertEqual(data['error'], 'An error occured in trying to login the user')

    def test_for_missing_password_key_on_attempt_to_login(self):
        """tests for a missing password key when user attempts to login"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.missing_password_key))
        data = json.loads(login_response.data)
        self.assertEqual(login_response.status_code, 400)
        self.assertEqual(data['error'], 'An error occured in trying to login the user')

    def test_for_missing_email_value_on_attempt_to_login(self):
        """tests for a missing email value when user attempts to login"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.missing_email_value))
        data = json.loads(login_response.data)
        self.assertEqual(login_response.status_code, 400)
        self.assertEqual(data['error'], 'An error occured in trying to login the user')

    def test_for_missing_password_value_on_attempt_to_login(self):
        """tests for a missing password value when user attempts to login"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.missing_password_value))
        data = json.loads(login_response.data)
        self.assertEqual(login_response.status_code, 400)
        self.assertEqual(data['error'], 'An error occured in trying to login the user')

    def test_for_empty_string_as_value_for_email(self):
        """tests for an empty email when user attempts to login"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.empty_string))
        data = json.loads(login_response.data)
        self.assertEqual(login_response.status_code, 400)
        self.assertEqual(data['error'], 'An error occured in trying to login the user')




    