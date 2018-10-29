from flask import Flask
from os import environ

api = Flask(__name__)

api.config['TEST_DB'] = environ.get('TESTING_ENVIRONMENT')


