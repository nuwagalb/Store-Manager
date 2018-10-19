import unittest
from flask import json, jsonify
from app import api

class GetSaleTestCase(unittest.TestCase):
    """
        contains tests for the GET SALE API ENDPOINT
    """
    def setUp(self):
        """sets up a new wsgi instance and a new get request to get a single sale"""
        self.api = api.test_client()
        self.api.get('/api/v1/sales/1', content_type="application/json")

    def test_success_code_on_get_sale_with_given_product_key(self):
        """tests for success on returning all product lessons"""
        response = self.api.get('/api/v1/sales/1', content_type='application/json')
        self.assertEqual(response.status_code, 200)
    