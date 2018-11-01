# import unittest
# from flask import json, jsonify, make_response
# from app import api

# class GetProductTestCase(unittest.TestCase):
#     """
#         contains tests for the GET PRODUCT API ENDPOINT
#     """
#     def setUp(self):
#         """sets up a new wsgi instance and a new get request to get a single product"""
#         self.api = api.test_client()
#         self.api.get('/api/v1/products/1', content_type="application/json")

#     def test_success_code_on_get_product_with_given_product_key(self):
#         """tests for success on returning a single record"""
#         response = self.api.get('/api/v1/products/1', content_type='application/json')
#         self.assertEqual(response.status_code, 200)
    