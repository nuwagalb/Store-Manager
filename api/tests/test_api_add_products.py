import unittest
from flask import json, jsonify
from app import api

class AddProductTestCase(unittest.TestCase):
    """
        contains tests for the ADD PRODUCT API ENDPOINT
    """
    def setUp(self):
        """sets up a new wsgi instance and a new post request to add a product"""
        self.api = api.test_client()
        self.api.post('/api/v1/products', content_type="application/json",
                      data=json.dumps({"name": "Nokia 3", "price": 341.62, "quantity": 6.00})
                 )

    def test_for_missing_name_key(self):
        """tests for missing name key"""
        response = self.api.post('/api/v1/products', content_type='application/json',
                                data=json.dumps({"": "Nokia 3", "price": 341.62, "quantity": 6.00}))

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Request is missing the product name key')

    def test_for_missing_price_key(self):
        """tests for missing price key"""
        response = self.api.post('/api/v1/products', content_type='application/json',
                                 data=json.dumps({"name": "Nokia 3", "": 341.62, "quantity": 6.00}))

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Request is missing the product price key')

    def test_for_missing_quantity_key(self):
        """tests for missing quantity key"""
        response = self.api.post('/api/v1/products', content_type='application/json',
                                 data=json.dumps({"name": "Nokia 3", "price": 341.62, "": 6.00}))

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Request is missing the product quantity key')

    def test_for_extra_keys_passed_to_the_request(self):
        """tests for extra keys passed in request"""
        response = self.api.post('/api/v1/products', content_type='application/json',
                                 data=json.dumps({"name": "Nokia 3", "price": 341.62,
                                                  "quantity": 6.00, "password": 'sql'})
                    )

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Request has more keys than expected')

    def test_for_invalid_type_of_data_passed_to_the_name_key(self):
        """tests for a non string passed as value for name key request"""
        response = self.api.post('/api/v1/products', content_type='application/json',
                                 data=json.dumps({"name": 5673, "price": 341.62, "quantity": 6.00}))

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Invalid data type for name value. Please enter a string')

    def test_for_empty_name_details(self):
        """tests for empty name details"""
        response = self.api.post('/api/v1/products', content_type='application/json',
                                 data=json.dumps({"name": '', "price": 341.62, "quantity": 6.00}))

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'The name of the product cannot be empty')

    def test_for_invalid_type_of_data_passed_to_the_price_key(self):
        """tests for a string passed as value for price key request"""
        response = self.api.post('/api/v1/products', content_type='application/json',
                                 data=json.dumps({"name": 'Nokia 3', "price": '341.62', "quantity": 6.00}))

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Invalid data type for price value. Please enter a float')

    def test_for_empty_price_details(self):
        """tests for empty price details"""
        response = self.api.post('/api/v1/products', content_type='application/json',
                                 data=json.dumps({"name": 'Nokia 3', "price": 0.00, "quantity": 6.00}))

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'The price of the product cannot be empty')

    def test_for_price_value_being_greater_than_zero(self):
        """tests for negative price details"""
        response = self.api.post('/api/v1/products', content_type='application/json',
                                 data=json.dumps({"name": 'Nokia 3', "price": -5.43, "quantity": 6.00}))

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'The price of the product cannot be zero or less than zero')

    def test_for_invalid_type_of_data_passed_to_the_quantity_key(self):
        """tests for a string passed as value for quantity key request"""
        response = self.api.post('/api/v1/products', content_type='application/json',
                                 data=json.dumps({"name": 'Nokia 3', "price": 341.62, "quantity": '6.00'}))

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Invalid data type for quantity value. Please enter a float')

    def test_for_empty_quantity_details(self):
        """tests for empty quantity details"""
        response = self.api.post('/api/v1/products', content_type='application/json',
                                 data=json.dumps({"name": 'Nokia 3', "price": 341.62, "quantity": 0.00}))

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'The quantity of the product cannot be empty')

    def test_for_quantity_value_being_greater_than_zero(self):
        """tests for negative quantity details"""
        response = self.api.post('/api/v1/products', content_type='application/json',
                                 data=json.dumps({"name": 'Nokia 3', "price": 341.62, "quantity": -6.00}))

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'The quantity of the product cannot be zero or less than zero')

    def test_for_successful_addition_of_a_product(self):
        """tests for successfully adding a product"""
        response = self.api.post('/api/v1/products', content_type='application/json',
                                 data=json.dumps({"name": 'Nokia 3', "price": 341.62, "quantity": 6.00}))
                 
        self.assertEqual(response.status_code, 201)