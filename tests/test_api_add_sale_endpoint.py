import unittest
from flask import json
from app import api
from db_helper import DBHelper
from models.users import User

class AddSaleTestCase(unittest.TestCase):
    """
        contains tests for the ENDPOINT OF ADDING A NEW SALE
    """
    def setUp(self):
        """sets up a new wsgi instance"""
        self.client = api.test_client()
        self.user_instance = User("admin@storemanager.com", "Admin@123", "admin")
        self.valid_user_details = {'email': 'admin@storemanager.com', 'password': 'Admin@123'}
        self.valid_product_details = {'name': 'Router', 'unit_price': 200, 'quantity': 40}
        self.valid_sales_details = {'product_id': 1, 'quantity': 10}
        self.valid_sales_details_two = {'product_id': 1, 'quantity': 40}
        self.missing_product_id_value = {'product_id': 0, 'quantity': 10}
        self.missing_quantity_value = {'product_id': 1, 'quantity': 0}
        self.negative_sale_details = {'product_id': 1, 'quantity': -2}
        self.excess_sale_details = {'product_id': 1, 'quantity': 80}
        self.missing_product_id_key = {' ': 1, 'quantity': 10}
        self.missing_quantity_key = {'product_id': 1, '': 10}
        self.sales_attendant = {'email': 'attendant@storemanager.com', 'password': 'Attendant@123'}        
    
    def tearDown(self):
        """creates and drops tables used in testing"""
        self.db = DBHelper('users', ['user_id', 'email', 'password', 'role'])
        self.db.drop_users_test_table()
        self.db.create_users_test_table()
        
        self.product_db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        self.product_db.drop_products_test_table()
        self.product_db.create_products_test_table()

    def test_sales_attendant_successfully_adds_a_new_sale(self):
        """tests that the sales attendant successfully adds a new sale"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        reg_response = self.client.post('api/v2/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})
        
        add_product_response = self.client.post('api/v2/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_login = self.client.post('api/v2/auth/login',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_data = json.loads(attendant_login.data)
        attendant_token =  attendant_data['token']

        add_sale_response = self.client.post('api/v2/sales',
                                content_type="application/json",
                                data=json.dumps(self.valid_sales_details),
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})
        
        data = json.loads(add_sale_response.data)
        self.assertEqual(add_sale_response.status_code, 201)
        self.assertEqual(data['Product id'], 1)
        self.assertEqual(data['Quantity left in stock'], 30)
        self.assertEqual(data['Quantity sold'], 10)
        self.assertEqual(data['Total Amount of Sale'], 2000)


    def test_that_the_admin_is_not_authorized_to_add_a_Sale(self):
        """tests for unauthorized access of the ADD SALE endpoint by the admin"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        add_sale_response = self.client.post('api/v2/sales',
                                content_type="application/json",
                                data=json.dumps(self.valid_sales_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})
        
        data = json.loads(add_sale_response.data)
        self.assertEqual(add_sale_response.status_code, 403)
        self.assertEqual(data['error'], 'Access to this resource is forbidden')

    def test_that_error_message_is_raised_when_no_product_id_value_is_specified_for_a_given_sale(self):
        """tests that an error message is raised when a product to sale is not specified"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        reg_response = self.client.post('api/v2/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})
        
        add_product_response = self.client.post('api/v2/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_login = self.client.post('api/v2/auth/login',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_data = json.loads(attendant_login.data)
        attendant_token =  attendant_data['token']

        add_sale_response = self.client.post('api/v2/sales',
                                content_type="application/json",
                                data=json.dumps(self.missing_product_id_value),
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})
        
        data = json.loads(add_sale_response.data)
        self.assertEqual(add_sale_response.status_code, 400)
        self.assertEqual(data['error'], 'You need to provide a product id')

    def test_that_error_message_is_raised_when_no_quantity_value_is_specified_for_a_given_sale(self):
        """tests that an error message is raised when a product to sale is not specified"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        reg_response = self.client.post('api/v2/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})
        
        add_product_response = self.client.post('api/v2/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_login = self.client.post('api/v2/auth/login',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_data = json.loads(attendant_login.data)
        attendant_token =  attendant_data['token']

        add_sale_response = self.client.post('api/v2/sales',
                                content_type="application/json",
                                data=json.dumps(self.missing_quantity_value),
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})
        
        data = json.loads(add_sale_response.data)
        self.assertEqual(add_sale_response.status_code, 400)
        self.assertEqual(data['error'], 'You need to provide a quantity for the product')

    def test_that_sale_quantity_value_can_not_be_negative(self):
        """tests that sale quantity cannot be negative"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        reg_response = self.client.post('api/v2/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})
        
        attendant_login = self.client.post('api/v2/auth/login',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_data = json.loads(attendant_login.data)
        attendant_token =  attendant_data['token']

        add_sale_response = self.client.post('api/v2/sales',
                                content_type="application/json",
                                data=json.dumps(self.negative_sale_details),
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})

        data = json.loads(add_sale_response.data)
        self.assertEqual(add_sale_response.status_code, 400)
        self.assertEqual(data['error'], 'Product quantity cannot be negative')

    def test_error_message_is_raised_when_trying_to_create_a_sale_for_a_none_existant_product(self):
        """tests for error on trying to create a sale for a none existant product"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        reg_response = self.client.post('api/v2/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_login = self.client.post('api/v2/auth/login',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_data = json.loads(attendant_login.data)
        attendant_token =  attendant_data['token']

        add_sale_response = self.client.post('api/v2/sales',
                                content_type="application/json",
                                data=json.dumps(self.valid_sales_details),
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})
        
        data = json.loads(add_sale_response.data)
        self.assertEqual(add_sale_response.status_code, 404)
        self.assertEqual(data['error'], 'Product does not exist. Please enter valid product id')

    def test_error_message_is_raised_when_quantity_to_make_sale_for_is_out_of_stock(self):
        """tests for trying to sale quantity that is out of stock"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        reg_response = self.client.post('api/v2/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})
        
        add_product_response = self.client.post('api/v2/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_login = self.client.post('api/v2/auth/login',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_data = json.loads(attendant_login.data)
        attendant_token =  attendant_data['token']

        add_sale_response = self.client.post('api/v2/sales',
                                content_type="application/json",
                                data=json.dumps(self.valid_sales_details_two),
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})

        add_sale_response_two = self.client.post('api/v2/sales',
                                content_type="application/json",
                                data=json.dumps(self.valid_sales_details_two),
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})
        
        data = json.loads(add_sale_response_two.data)
        self.assertEqual(add_sale_response_two.status_code, 404)
        self.assertEqual(data['error'], 'There are no products to sell')

    def test_for_an_error_message_when_quantity_requested_for_is_more_than_that_in_stock(self):
        """tests that quantity requested for cannot be greater than that in stock"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        reg_response = self.client.post('api/v2/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})
        
        add_product_response = self.client.post('api/v2/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_login = self.client.post('api/v2/auth/login',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_data = json.loads(attendant_login.data)
        attendant_token =  attendant_data['token']

        add_sale_response = self.client.post('api/v2/sales',
                                content_type="application/json",
                                data=json.dumps(self.excess_sale_details),
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})

        data = json.loads(add_sale_response.data)
        self.assertEqual(add_sale_response.status_code, 404)
        self.assertEqual(
            data['error'],
            'The quantity you requested for is more than that in stock'
        )

    def test_error_message_is_raised_when_new_sale_details_are_not_inserted_in_the_database(self):
        """tests that adding a sale raises an error if record is not inserted in the database"""
        login_response = self.client.post('api/v2/auth/login', content_type="application/json",
                            data=json.dumps(self.valid_user_details))

        login_data = json.loads(login_response.data)
        token = login_data['token']

        reg_response = self.client.post('api/v2/auth/signup',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})
        
        add_product_response = self.client.post('api/v2/products',
                                content_type="application/json",
                                data=json.dumps(self.valid_product_details),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_login = self.client.post('api/v2/auth/login',
                                content_type="application/json",
                                data=json.dumps(self.sales_attendant),
                                headers={'Authorization': 'Bearer {}'.format(token)})

        attendant_data = json.loads(attendant_login.data)
        attendant_token =  attendant_data['token']

        add_sale_response = self.client.post('api/v2/sales',
                                content_type="application/json",
                                data=json.dumps(self.valid_sales_details),
                                headers={'Authorization': 'Bearer {}'.format(attendant_token)})
        data = json.loads(add_sale_response.data)
        
        db = DBHelper('sales', ['sale_id', 'product_id', 'quantity', 'total_amount', 'user_id'])
        inserted_record = db.find_record_by_id(1)

        if not inserted_record:
            self.assertEqual(add_sale_response.status_code, 400)
            self.assertEqual(
                data['error'],
                'Sale order could not be created'
            )

    



    

