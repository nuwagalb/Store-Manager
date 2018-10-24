# Store-Manager
An application that helps store owners manage sales and product inventory records 
in a single store


#### Badges
[![Build Status](https://travis-ci.com/nuwagalb/Store-Manager.svg?branch=feat_get_all_sales_endpoint)](https://travis-ci.com/nuwagalb/Store-Manager) [![Coverage Status](https://coveralls.io/repos/github/nuwagalb/Store-Manager/badge.svg?branch=feat_get_all_sales_endpoint)](https://coveralls.io/github/nuwagalb/Store-Manager?branch=feat_get_all_sales_endpoint) [![Maintainability](https://api.codeclimate.com/v1/badges/27f79698c2b829a29651/maintainability)](https://codeclimate.com/github/nuwagalb/Store-Manager/maintainability)

#### project captures the following routes 

| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| POST | /api/v1/products | Add a product |
| POST | api/v1/sales | Add a sale |
| GET | api/v1/products<_productId_> | Get a product |
| GET | api/v1/sales/<_saleId_> | Get a sale |
| GET | api/v1/sales | Get all sales |
| GET | api/v1/products | Get all sales |

#### Technologies and Tools used to develop this App

1. Python
2. VSCODE (for editing and debugging)
3. Flask micro framework
4. Postman for testing endpoints


#### The application is Hosted at Heroku on the link below.
https://store-manager-v1-api.herokuapp.com/

#### Set up project to get it up and running

clone repository from link below

1. $ https://github.com/nuwagalb/Store-Manager/tree/feat_get_all_sales_endpoint
2. $ cd Store-Manager

#### Set up Virtual environment by running commands below

- virtualenv -p python3 venv
- source venv/bin/activate (for linux)

#### Install all project dependencies by running the command below.

$ pip install -r requirements.txt

#### To run the unit tests invoke/run the command below.

$ pytest

#### or for detailed output on unit tests run.

$ py.test --cov=api tests/

#### To run the application invoke the command below.

$ python app.py

#### Now that the server is running , open your browser and run one of the links below.

$ localhost:5000 or 127.0.0.1:5000
You can now test out the links using Postman API Development and Testing tool

