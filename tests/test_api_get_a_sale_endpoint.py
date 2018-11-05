import unittest
from flask import json
from app import api
from db_helper import DBHelper
from models.users import User

class GetSingleSaleTestCase(unittest.TestCase):
    """
        contains tests for the ENDPOINT OF GETTING A SINGLE SALE
    """
    def setUp(self):
        """sets up a new wsgi instance"""
        self.client = api.test_client()
        self.user_instance = User("admin@storemanager.com", "Admin@123", "admin")
        self.valid_user_details = {'email': 'admin@storemanager.com', 'password': 'Admin@123'}
        self.sales_attendant = {'email': 'attendant@storemanager.com', 'password': 'Attendant@123'} 
        self.valid_product_details = {'name': 'Navision Laptop', 'unit_price': 2000, 'quantity': 100}
        self.valid_sale = {'product_id': 1, 'quantity': 10}
        
    
    def tearDown(self):
        """creates and drops tables used in testing"""
        self.db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        self.db.drop_users_test_table()
        self.db.create_users_test_table()
        
        self.product_db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        self.product_db.drop_products_test_table()
        self.product_db.create_products_test_table()

        self.sale_db = DBHelper('sales', ['sale_id', 'product_id', 'quantity', 'total_amount', 'user_id'])
        self.sale_db.drop_sales_test_table()
        self.sale_db.create_sales_test_table()

    def test_that_authorized_user_can_successfully_get_a_single_sale(self):
        """tests that an authorized user can successfully get a single sale"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        add_product_response = self.client.post('api/v2/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        reg_response = self.client.post('api/v2/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_login = self.client.post('api/v2/auth/login', content_type="application/json",
                                    data=json.dumps(self.sales_attendant))

        attendant_data = json.loads(attendant_login.data)
        attendant_token = attendant_data['token']

        add_sale_response = self.client.post('api/v2/sales',
                                content_type="application/json",
                                data=json.dumps(self.valid_sale),
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})
        
        get_single_sale_response = self.client.get('api/v2/sales/1',
                                content_type="application/json",
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})

        data = json.loads(get_single_sale_response.data)
        self.assertEqual(get_single_sale_response.status_code, 200)
        self.assertEqual(data['product_id'], 1)
        self.assertEqual(data['quantity'], 10)
        self.assertEqual(data['sale_id'], 1)
        self.assertEqual(data['total_amount'], 20000)
        self.assertEqual(data['user_id'], 2)

    def test_that_an_error_message_is_raised_when_getting_a_none_existent_sale(self):
        """tests that an error message is raised on getting a none existent sale"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        get_single_sale_response = self.client.get('api/v2/sales/1',
                                content_type="application/json",
                                headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(get_single_sale_response.data)
        self.assertEqual(get_single_sale_response.status_code, 404)
        self.assertEqual(data['error'], 'The sale you are trying to fetch does not exist')
        
    