from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models.products import Product
from models.sales import Sale
from models.users import User
from models.validators import Validator
import datetime
from db_helper import DBHelper

api = Flask(__name__)

api.config['JWT_SECRET_KEY'] = '89#456612dfmrprkp'

jwt = JWTManager(api)

@api.route("/")
def index():
    """returns the index.html template"""
    role = request.args.get('role')

    if not role:
        role = "Visitor"

    return render_template('index.html', role=role)

@api.route("/api/v1/auth/login", methods=["POST"])
def login():
    """logs in a user"""
    response = None

    json_data = request.get_json()
    email = json_data['email']
    password = json_data['password']

    user = User(email, password)
    user.initial_login()
    
    returned_user = user.get_email(email)
    current_password = user.get_password(email)

    if not returned_user:
       return jsonify({'message': 'Invalid email address.'})

    if not check_password_hash(current_password, password):
        return jsonify({'message': 'Invalid password. Please enter the correct password'})
    
    token = create_access_token(identity=returned_user, expires_delta=datetime.timedelta(hours=8))
    return jsonify({'message': '{} was successfully logged in'.format(email)})

@api.route("/api/v1/auth/signup", methods=["POST"])
@jwt_required
def signup():
    """signs up a user"""
    try:
        response = None
        json_data = request.get_json()

        email = json_data.get('email')
        password = json_data.get('password')

        email_status = Validator.validate_email(email)
        password_status = Validator.validate_password(password)

        if email_status is True:
            if password_status is True:
                password_hash = generate_password_hash(password)

                user = User(email, password_hash)
                registration_status = user.register()

                if not registration_status:
                    response = {'message': 'User details could not be registered'}

                response = {'message': registration_status}
                return jsonify(response)

            return jsonify({'message': password_status})

        return jsonify({'message': email_status})
    except:
        return jsonify({'message': 'There was an error in trying to register a user'})

#PRODUCTS
#add new product
@api.route("/api/v1/products", methods=['POST'])
@jwt_required
def add_product():
    """adds new product"""
    try:
        json_data = request.get_json()

        name = json_data['name']
        unit_price = json_data['unit_price']
        quantity = json_data['quantity']

        if name and unit_price and quantity:
            new_product = Product(name, unit_price, quantity)
            product_status = new_product.add_product()
            
            if not product_status:
                response = {'message': 'Product could not be added'}

            response = {'message': product_status}
            return jsonify(response)

        return jsonify(product_status)
    except:
        return jsonify({'message': 'There was an error in trying to add a product'})

#get a single product
@api.route("/api/v1/products/<int:productId>", methods=['GET'])
@jwt_required
def get_a_product(productId):
    """returns a single product"""
    try:
        response = Product.get_single_product(productId)
        if not response:
            response = jsonify({'message': 'The product no products in fetch'})
        return jsonify({'message': response})
    except:
        return jsonify({'message': 'There was an error in trying to fetch the product'})

#get all product
@api.route("/api/v1/products", methods=['GET'])
@jwt_required
def get_all_products():
    """returns all products"""
    try:
        response = Product.get_all_products()
        if not response:
            response = jsonify({'message': 'There are no products to fetch'})
        return jsonify(response)
    except:
        return jsonify({'message': 'There was an error in trying to fetch products'})

#SALES
#add new sale
@api.route("/api/v1/sales", methods=['POST'])
def add_sale():
    """adds new sale"""
    json_data = request.get_json()

    try:
        if 'product_id' not in json_data:
            response_object = {'message': 'Request is missing the product id key'}
            status_code = 400

        elif 'quantity' not in json_data:
            response_object = {'message': 'Request is missing the sale quantity key'}
            status_code = 400

        elif 'amount' not in json_data:
            response_object = {'message': 'Request is missing the sale amount key'}
            status_code = 400

        elif len(json_data.keys()) > 3:
            response_object = {'message': 'Request has more keys than expected'}
            status_code = 400

        else:
            new_sale = Sale(json_data['product_id'], json_data['quantity'], json_data['amount'])
            sale_status = new_sale.add_sale()
            
            if sale_status is True:
                response_object = Sale.all_sales[-1]
                status_code = 201

        return jsonify(response_object), status_code
    except:
        response_object = {'message':  'Invalid sale request'}
        return jsonify(response_object)

#get a single sale
@api.route("/api/v1/sales/<int:saleId>", methods=['GET'])
def get_a_sale(saleId):
    """returns a single product"""
    try:
        if not Sale.all_sales:
            return jsonify({'message':  'There are currently no sale records'})

        for sale in Sale.all_sales:
            if sale.get('sale_id') == saleId:
                return jsonify(sale), 200
        
        return jsonify(response_object)
    except:
        response_object = {'message':  'Invalid request'}
        return jsonify(response_object)

#get all sales
@api.route("/api/v1/sales", methods=['GET'])
def get_all_sales():
    """returns all sales"""
    try:
        if not Sale.all_sales:
            return jsonify({'message':  'There are currently no sale records'})
        return jsonify(Sale.all_sales)
    except:
        response_object = {'message':  'Invalid request'}
        return jsonify(response_object)

#ERROR HANDLERS
@api.errorhandler(400)
def bad_request(error):
    """displays error msg when 400 error code is raised"""
    return jsonify({'message': 'A Bad request was sent to the server'}), 400

@api.errorhandler(404)
def page_not_found(error):
    """displays error msg when 404 error code is raised"""
    return jsonify({'message': 'Resource could not be found'}), 404

@api.errorhandler(401)
def unauthorized_access(error):
    """displays error message when 401 error code is raised"""
    return jsonify({'message': 'You are not authorized to access this resource'}), 401

@api.errorhandler(500)
def internal_server_error(error):
    """displays error message when 500 error code is raised"""
    return jsonify({'message': 'An internal server error was encountered'}), 404

@api.errorhandler(405)
def wrong_method(error):
    """displays error message when 405 error code is raised"""
    return jsonify({'message': 'You tried to access the resource using the wrong method.'}), 405