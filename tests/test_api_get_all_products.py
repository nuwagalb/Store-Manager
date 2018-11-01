# import unittest
# from flask import json, jsonify, make_response
# from app import api

# class GetAllProductsTestCase(unittest.TestCase):
#     """
#         contains tests for the GET ALL PRODUCTS API ENDPOINT
#     """
#     def setUp(self):
#         """sets up a new wsgi instance and a get request to get all products"""
#         self.api = api.test_client()
#         self.api.get('/api/v1/products', content_type="application/json")

#     def test_success_code_returned_on_getting_all_products(self):
#         """tests for success on returning a single record"""
#         response = self.api.get('/api/v1/products', content_type='application/json')
#         self.assertEqual(response.status_code, 200)
    