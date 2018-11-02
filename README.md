# Store-Manager
An application that helps store owners manage sales and product inventory records 
in a single store


#### Badges

#### project captures the following routes 

| REQUEST | ROUTE | FUNCTIONALITY |
| ------- | ----- | ------------- |
| POST | api/v1/products | Add a product |
| POST | api/v1/sales | Add a sale |
| POST | api/v1/auth/signup | Register a user |
| POST | api/v1/auth/login | Login a user |
| PUT | api/v1/products/<_productId_> | Update a Product |
| DELETE | api/v1/products/<_productId_> | Delete a Product |
| GET | api/v1/products<_productId_> | Get a product |
| GET | api/v1/sales/<_saleId_> | Get a sale |
| GET | api/v1/sales | Get all sales |
| GET | api/v1/products | Get all products |
| 

#### Technologies and Tools used to develop this App

1. Python
2. VSCODE (for editing and debugging)
3. Flask micro framework
4. Postman for testing endpoints
5. Postgres for storing data


#### The application is Hosted at Heroku on the link below.
https://store-manager-v1-api.herokuapp.com/

#### Set up project to get it up and running

clone repository from link below

1. $ https://github.com/nuwagalb/Store-Manager.git
2. $ cd Store-Manager

#### Set up Virtual environment by running commands below

- virtualenv -p python3 venv
- source venv/bin/activate (for linux)

#### Install all project dependencies by running the command below.

$ pip install -r requirements.txt

#### To setup the database and associated tables, run
1. Edit the db_config.py file to include details for making 
   a connection to your postgres DBMS
2. Run the db_setup.py file to create the database and tables
   $ python db_setup.py

#### To run the unit tests invoke/run the command below.
1. $ source .env - this sets up an environment variable that gives you access to the test database
2. $ pytest

#### or for detailed output on unit tests run.

$ py.test --cov=api tests/

#### to move out of the testing environment, run
$ unset APP_SETTINGS

#### To run the application invoke the command below.

$ python app.py

#### Now that the server is running , open your browser and run one of the following links.

$ localhost:5000 or 127.0.0.1:5000
- You can now test out the endpoints

#### The default login details are:
- Email Address: admin@storemanager.com
- Password: Admin@123

