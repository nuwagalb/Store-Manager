import unittest
from flask import json, jsonify
from app import api
from db_helper import DBHelper

class RegisterUserTestCase(unittest.TestCase):
    """
        contains tests for the REGISTER USER API ENDPOINT
    """
    def setUp(self):
        """sets up a new wsgi instance and a new post request to add a sale"""
        self.api = api.test_client()
        self.admin = {"email": "isnuwa@gmail.com", "password": "Nuwag@1j"}
        self.reg_details = {
            "email": "nuwagalb@yahoo.com", 
            "password": 'nuwagalb'}


    def test_for_initial_successful_registration_of_the_admin(self):
        """tests that a user has been successfully registered"""
        login_response = self.api.post('/api/v1/auth/login', content_type="application/json",
                      data=json.dumps(self.admin)
                 )
        data = login_response.json
        token = data['Token']

        register_user = self.api.post('api/v1/auth/login', content_type="application/json",
                            data={}, headers={'Authorization': 'Bearer {}'.format(token)}
                        )
        self.assertEqual(login_response.status_code, 201)
        self.assertEqual(data['message'], "isnuwa@gmail.com successfully created")

    