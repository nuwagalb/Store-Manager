import unittest
from flask import json
from app import api
from db_helper import DBHelper
from models.users import User

class DeleteProductTestCase(unittest.TestCase):
    """
        contains tests for THE ENDPOINT THAT DELETES A PRODUCT
    """
    def setUp(self):
        """sets up a new wsgi instance"""
        self.client = api.test_client()
        self.user_instance = User("admin@storemanager.com", "Admin@123", "admin")
        self.valid_user_details = {'email': 'admin@storemanager.com', 'password': 'Admin@123'}
        self.valid_product_details = {'name': 'Laser Jet Printer', 'unit_price': 400, 'quantity': 20}
        self.sales_attendant = {'email': 'attendant@storemanager.com', 'password': 'Attendant@123'}
        
    def tearDown(self):
        """creates and drops tables used in testing"""
        self.db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        self.db.drop_users_test_table()
        self.db.create_users_test_table()
        
        self.product_db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        self.product_db.drop_products_test_table()
        self.product_db.create_products_test_table()


    def test_that_an_admin_can_successfully_delete_a_product(self):
        """tests that an admin can successfully delete a product"""
        login_response = self.client.post('api/v1/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        add_product_response = self.client.post('api/v1/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})        
        
        delete_product_response = self.client.delete('api/v1/products/1',
                                content_type="application/json",
                                headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(delete_product_response.data)
        self.assertEqual(delete_product_response.status_code, 200)
        self.assertEqual(data['message'], 'Laser Jet Printer was successfully deleted')

    def test_that_an_error_message_is_raised_when_trying_to_delete_a_none_existent_product(self):
        """tests that an error message is raised on trying to delete a none existent product"""
        login_response = self.client.post('api/v1/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']       
        
        delete_product_response = self.client.delete('api/v1/products/1',
                                content_type="application/json",
                                headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(delete_product_response.data)
        self.assertEqual(delete_product_response.status_code, 404)
        self.assertEqual(
            data['error'],
            'The product you tried to delete does not exist'
        )

    def test_that_a_sale_attendant_can_not_delete_a_product(self):
        """tests that a sale attendant has no access to delete a product"""
        login_response = self.client.post('api/v1/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        reg_response = self.client.post('api/v1/auth/signup',
                            content_type="application/json",
                            data=json.dumps(self.sales_attendant),
                            headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_login = self.client.post('api/v1/auth/login', content_type="application/json",
                            data=json.dumps(self.sales_attendant))

        attendant_data = json.loads(attendant_login.data)
        attendant_token = attendant_data['token']
                       
        delete_product_response = self.client.delete('api/v1/products/1',
                                content_type="application/json",
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})

        data = json.loads(delete_product_response.data)
        self.assertEqual(delete_product_response.status_code, 403)
        self.assertEqual(
            data['error'],
            'Access to this resource is forbidden'
        )

    