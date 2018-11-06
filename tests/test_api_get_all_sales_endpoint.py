import unittest
from flask import json
from app import api
from db_helper import DBHelper
from models.users import User

class GetAllSalesTestCase(unittest.TestCase):
    """
        contains tests for the ENDPOINT OF GETTING ALL SALES
    """
    def setUp(self):
        """sets up a new wsgi instance"""
        self.client = api.test_client()
        self.user_instance = User("admin@storemanager.com", "Admin@123", "admin")
        self.valid_user_details = {'email': 'admin@storemanager.com', 'password': 'Admin@123'}
        self.sales_attendant = {'email': 'attendant@storemanager.com', 'password': 'Attendant@123'} 
        self.valid_product_details = {'name': 'Navision Laptop', 'unit_price': 2000, 'quantity': 100}
        self.valid_product_2_details = {'name': 'Acer Laptop', 'unit_price': 500, 'quantity': 40}
        self.valid_sale = {'product_id': 1, 'quantity': 50}
        self.valid_sale_2 = {'product_id': 2, 'quantity': 20}
        
    def tearDown(self):
        """creates and drops tables used in testing"""
        self.db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        self.db.drop_users_test_table()
        self.db.create_users_test_table()
        
        self.product_db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        self.product_db.drop_products_test_table()
        self.product_db.create_products_test_table()


    def test_that_authorized_user_can_successfully_get_all_sales(self):
        """tests that an authorized user can successfully get a all sales"""
        login_response = self.client.post('api/v1/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        add_product_response_one = self.client.post('api/v1/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        add_product_response_two = self.client.post('api/v1/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_2_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        reg_response = self.client.post('api/v1/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_login = self.client.post('api/v1/auth/login', content_type="application/json",
                                    data=json.dumps(self.sales_attendant))

        attendant_data = json.loads(attendant_login.data)
        attendant_token = attendant_data['token']

        add_sale_response = self.client.post('api/v1/sales',
                                content_type="application/json",
                                data=json.dumps(self.valid_sale),
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})

        add_sale_response_two = self.client.post('api/v1/sales',
                                content_type="application/json",
                                data=json.dumps(self.valid_sale_2),
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})       
        
        get_all_sales_response = self.client.get('api/v1/sales',
                                content_type="application/json",
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})

        data = json.loads(get_all_sales_response.data)
        self.assertEqual(get_all_sales_response.status_code, 200)
        self.assertEqual(data[0].get('product_id'), 1)
        self.assertEqual(data[0].get('quantity'), 50)
        self.assertEqual(data[0].get('sale_id'), 1)
        self.assertEqual(data[0].get('total_amount'), 100000)
        self.assertEqual(data[0].get('user_id'), 2)
        self.assertEqual(data[1].get('product_id'), 2)
        self.assertEqual(data[1].get('quantity'), 20)
        self.assertEqual(data[1].get('sale_id'), 2)
        self.assertEqual(data[1].get('total_amount'), 10000)
        self.assertEqual(data[1].get('user_id'), 2)

    def test_that_an_error_message_is_raised_when_getting_empty_sales(self):
        """tests that an error message is raised on getting empty sales"""
        login_response = self.client.post('api/v1/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        get_all_sales_response = self.client.get('api/v1/sales',
                                content_type="application/json",
                                headers={'Authorization': 'Bearer {}'.format(token)})

        data = json.loads(get_all_sales_response.data)
        self.assertEqual(get_all_sales_response.status_code, 404)
        self.assertEqual(
            data['error'],
            'There are no sales to fetch'
        )
        
    