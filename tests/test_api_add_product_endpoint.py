import unittest
from flask import json
from app import api
from db_helper import DBHelper
from models.users import User

class AddProductTestCase(unittest.TestCase):
    """
        contains tests for the ENDPOINT OF ADDING A PRODUCT
    """
    def setUp(self):
        """sets up a new wsgi instance"""
        self.client = api.test_client()
        self.user_instance = User("admin@storemanager.com", "Admin@123", "admin")
        self.valid_user_details = {'email': 'admin@storemanager.com', 'password': 'Admin@123'}
        self.valid_product_details = {'name': 'HP Pavilion', 'unit_price': 4000, 'quantity': 200}
        self.sales_attendant = {'email': 'attendant@storemanager.com', 'password': 'Attendant@123'}
        self.missing_name_key = {'': 'HP Pavilion', 'unit_price': 4000, 'quantity': 200}
        self.missing_unit_price_key = {'name': 'HP Pavilion', '': 4000, 'quantity': 200}
        self.missing_quantity_key = {'': 'HP Pavilion', 'unit_price': 4000, '': 200}
        self.missing_name_value = {'name': None, 'unit_price': 4000, 'quantity': 200}
        self.missing_unit_price_value = {'name': 'HP Pavilion', 'unit_price': None, 'quantity': 200}
        self.missing_quantity_value = {'name': 'HP Pavilion', 'unit_price': 4000, 'quantity': None}
        
    
    def tearDown(self):
        """creates and drops tables used in testing"""
        self.db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        self.db.drop_users_test_table()
        self.db.create_users_test_table()
        
        self.product_db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        self.product_db.drop_products_test_table()
        self.product_db.create_products_test_table()

    def test_admin_successfully_adds_a_new_product(self):
        """tests that the admin successfully adds a new product"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']        
        
        add_product_response = self.client.post('api/v2/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(add_product_response.data)
        self.assertEqual(add_product_response.status_code, 201)
        self.assertEqual(data['product_id'], 1)
        self.assertEqual(data['name'], 'HP Pavilion')
        self.assertEqual(data['unit_price'], 4000)
        self.assertEqual(data['quantity'], 200)

    def test_for_duplicate_entry_of_a_product(self):
        """tests that error message is raised when trying to enter add a product that already exists"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']        
        
        add_product_response_once = self.client.post('api/v2/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        add_product_response_twice = self.client.post('api/v2/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(add_product_response_twice.data)
        self.assertEqual(add_product_response_twice.status_code, 409)
        self.assertEqual(data['error'], 'Product already exists. Please select a different name')

    def test_that_store_attendant_can_not_add_a_product(self):
        """tests that a store attendant cannot add a product"""
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

        attendant_add_product_attempt = self.client.post('api/v2/products', 
                                    content_type="application/json",
                                    data=json.dumps(self.valid_product_details),
                                    headers={'Authorization': 'Bearer {}'.format(attendant_token)})

        data = json.loads(attendant_add_product_attempt.data)
        self.assertEqual(attendant_add_product_attempt.status_code, 403)
        self.assertEqual(
            data['error'],
            'Access to this resource is forbidden'
        )

    def test_for_missing_name_key_on_attempt_to_add_a_product(self):
        """tests for a missing name key when user attempts to add a product"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        add_product_response = self.client.post('api/v2/products', content_type="application/json",
                            data=json.dumps(self.missing_name_key),
                            headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(add_product_response.data)
        self.assertEqual(add_product_response.status_code, 400)
        self.assertEqual(data['error'], 'There was an error in trying to add a product')

    def test_for_missing_unit_price_key_on_attempt_to_add_a_product(self):
        """tests for a missing unit price key when user attempts to add a product"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        add_product_response = self.client.post('api/v2/products', content_type="application/json",
                            data=json.dumps(self.missing_unit_price_key),
                            headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(add_product_response.data)
        self.assertEqual(add_product_response.status_code, 400)
        self.assertEqual(data['error'], 'There was an error in trying to add a product')

    def test_for_missing_quantity_key_on_attempt_to_add_a_product(self):
        """tests for a missing quantity key when user attempts to add a product"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        add_product_response = self.client.post('api/v2/products', content_type="application/json",
                            data=json.dumps(self.missing_quantity_key),
                            headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(add_product_response.data)
        self.assertEqual(add_product_response.status_code, 400)
        self.assertEqual(data['error'], 'There was an error in trying to add a product')

    def test_for_missing_name_value_on_attempt_to_add_a_product(self):
        """tests for a missing name value when user attempts to add a product"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        add_product_response = self.client.post('api/v2/products', content_type="application/json",
                            data=json.dumps(self.missing_name_value),
                            headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(add_product_response.data)
        self.assertEqual(add_product_response.status_code, 400)
        self.assertEqual(data['error'], 'There was an error in trying to add a product')

    def test_for_missing_unit_price_value_on_attempt_to_add_a_product(self):
        """tests for a missing unit price value when user attempts to add a product"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        add_product_response = self.client.post('api/v2/products', content_type="application/json",
                            data=json.dumps(self.missing_unit_price_value),
                            headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(add_product_response.data)
        self.assertEqual(add_product_response.status_code, 400)
        self.assertEqual(data['error'], 'There was an error in trying to add a product')

    def test_for_missing_quantity_value_on_attempt_to_add_a_product(self):
        """tests for a missing quantity value when user attempts to add a product"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        add_product_response = self.client.post('api/v2/products', content_type="application/json",
                            data=json.dumps(self.missing_quantity_value),
                            headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(add_product_response.data)
        self.assertEqual(add_product_response.status_code, 400)
        self.assertEqual(data['error'], 'There was an error in trying to add a product')


    

    


    




        