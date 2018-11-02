import unittest
from flask import json, jsonify
from app import api
from db_helper import DBHelper

URL = 'api/v1'

class AddProductTestCase(unittest.TestCase):
    """
        contains tests for the REGISTER USER API ENDPOINT
    """
    def setUp(self):
        """sets up a new wsgi instance and a new post request to add a user"""
        self.client = api.test_client()
        self.db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        self.user1 = {"email": "admin@storemanager.com", "password": "Admin@123"}
        self.user2 = {"email": "store_attendant3@storemanager.com", "password": "Attendant@234"}
        self.product1 = {"name": "Sugar", "unit_price": 2300, "quantity": 25}