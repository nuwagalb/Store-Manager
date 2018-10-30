from flask import Flask, request, json, jsonify
from os import environ
from flask_jwt_extended import JWTManager
from werkzeug.security import generate_password_hash, check_password_hash

api = Flask(__name__)
api.config['TEST_DB'] = environ.get('TESTING_ENVIRONMENT')
jwt = JWTManager(api)

