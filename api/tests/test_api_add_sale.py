import unittest
from flask import json, jsonify
from app import api

class AddSaleTestCase(unittest.TestCase):
    """
        contains tests for the ADD SALE API ENDPOINT
    """
    def setUp(self):
        """sets up a new wsgi instance and a new post request to add a sale"""
        self.api = api.test_client()
        self.api.post('/api/v1/sales', content_type="application/json",
                      data=json.dumps({"product_id": 1, "quantity": 60, "amount": 600.00})
                 )

    def test_for_missing_product_id_key(self):
        """tests for missing product_id key"""
        response = self.api.post('/api/v1/sales', content_type='application/json',
                                data=json.dumps({"": 1, "quantity": 60, "amount": 600.00}))

        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Request is missing the product id key')

    def test_for_missing_quantity_key(self):
        """tests for missing  key"""
        response = self.api.post('/api/v1/sales', content_type='application/json',
                                 data=json.dumps({"product_id": 1, "": "20-09-18", "amount": 600.00}))

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Request is missing the sale quantity key')

    def test_for_missing_amount_key(self):
        """tests for missing amount key"""
        response = self.api.post('/api/v1/sales', content_type='application/json',
                                 data=json.dumps({"product_id": 1, "quantity": 60, "": 600.00}))

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Request is missing the sale amount key')

    def test_for_extra_keys_passed_to_the_request(self):
        """tests for extra keys passed in request"""
        response = self.api.post('/api/v1/sales', content_type='application/json',
                                 data=json.dumps({"product_id": 1, "quantity": 60,
                                                  "amount": 600.00, "password": 'sql'}
                            )
                    )

        data = json.loads(response.data)                   
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['message'], 'Request has more keys than expected')

    def test_for_successful_addition_of_a_sale(self):
        """tests for successfully adding a sale"""
        response = self.api.post('/api/v1/sales', content_type='application/json',
                                 data=json.dumps({"product_id": 1, "quantity": 60, "amount": 600.00}))
                 
        self.assertEqual(response.status_code, 201)