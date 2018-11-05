import unittest
from flask import json
from app import api
from db_helper import DBHelper
from models.users import User

class GetAllProductsTestCase(unittest.TestCase):
    """
        contains tests for the ENDPOINT OF GETTING ALL PRODUCTS
    """
    def setUp(self):
        """sets up a new wsgi instance"""
        self.client = api.test_client()
        self.user_instance = User("admin@storemanager.com", "Admin@123", "admin")
        self.valid_user_details = {'email': 'admin@storemanager.com', 'password': 'Admin@123'}
        self.valid_product_details_one = {'name': 'Mac Pro', 'unit_price': 2500, 'quantity': 350}
        self.valid_product_details_two = {'name': 'Samsung Edge', 'unit_price': 1000, 'quantity': 2000}
        
    def tearDown(self):
        """creates and drops tables used in testing"""
        self.db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        self.db.drop_users_test_table()
        self.db.create_users_test_table()
        
        self.product_db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        self.product_db.drop_products_test_table()
        self.product_db.create_products_test_table()


    def test_that_authorized_user_can_successfully_get_all_product(self):
        """tests that an authorized user can successfully get all product"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        add_product_response_one = self.client.post('api/v2/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details_one),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        add_product_response_two = self.client.post('api/v2/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details_two),
                                headers={'Authorization': 'Bearer {}'.format(token)})        
        
        get_all_product_response = self.client.get('api/v2/products',
                                content_type="application/json",
                                headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(get_all_product_response.data)
        self.assertEqual(get_all_product_response.status_code, 200)
        self.assertEqual(data[0].get('product_id'), 1)
        self.assertEqual(data[0].get('name'), 'Mac Pro')
        self.assertEqual(data[0].get('quantity'), 350)
        self.assertEqual(data[0].get('unit_price'), 2500)
        self.assertEqual(data[1].get('product_id'), 2)
        self.assertEqual(data[1].get('name'), 'Samsung Edge')
        self.assertEqual(data[1].get('quantity'), 2000)
        self.assertEqual(data[1].get('unit_price'), 1000)

    def test_that_an_error_message_is_raised_when_getting_empty_products(self):
        """tests that an error message is raised on getting empty products"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        get_all_products_response = self.client.get('api/v2/products',
                                content_type="application/json",
                                headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(get_all_products_response.data)
        self.assertEqual(get_all_products_response.status_code, 404)
        self.assertEqual(
            data['error'],
            'There are no products to fetch'
        )
        
    