import unittest
from flask import json
from app import api
from db_helper import DBHelper
from models.users import User

class GetSingleProductTestCase(unittest.TestCase):
    """
        contains tests for the ENDPOINT OF GETTING A SINGLE PRODUCT
    """
    def setUp(self):
        """sets up a new wsgi instance"""
        self.client = api.test_client()
        self.user_instance = User("admin@storemanager.com", "Admin@123", "admin")
        self.valid_user_details = {'email': 'admin@storemanager.com', 'password': 'Admin@123'}
        self.valid_product_details = {'name': 'HP Pavilion', 'unit_price': 4000, 'quantity': 200}
        
    
    def tearDown(self):
        """creates and drops tables used in testing"""
        self.db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        self.db.drop_users_test_table()
        self.db.create_users_test_table()
        
        self.product_db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        self.product_db.drop_products_test_table()
        self.product_db.create_products_test_table()


    def test_that_authorized_user_can_successfully_get_a_single_product(self):
        """tests that an authorized user can successfully get a single product"""
        login_response = self.client.post('api/v1/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        add_product_response = self.client.post('api/v1/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})        
        
        get_single_product_response = self.client.get('api/v1/products/1',
                                content_type="application/json",
                                headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(get_single_product_response.data)
        self.assertEqual(get_single_product_response.status_code, 200)
        self.assertEqual(data['product_id'], 1)
        self.assertEqual(data['name'], 'HP Pavilion')
        self.assertEqual(data['unit_price'], 4000)
        self.assertEqual(data['quantity'], 200)


    def test_that_an_error_message_is_raised_when_getting_a_non_existent_product(self):
        """tests that an error message is raised on getting a none existent product"""
        login_response = self.client.post('api/v1/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        get_single_product_response = self.client.get('api/v1/products/1',
                                content_type="application/json",
                                headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(get_single_product_response.data)
        self.assertEqual(get_single_product_response.status_code, 404)
        self.assertEqual(
            data['error'],
            'Invalid request. The product you are searching for does not exist'
        )
        
    