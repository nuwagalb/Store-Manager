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

@api.route("/api/v1/auth/login", methods=["POST"])
def login():
    """logs in a user"""
    try:
        json_data = request.get_json()
        email = json_data.get('email').strip()
        password = json_data.get('password').strip()

        user = User(email, password)

        returned_user = user.get_email(email)
        current_password = user.get_password(email)

        if not returned_user:
            return jsonify({'error': 'Invalid email address given'}), 401

        if not check_password_hash(current_password, password):
            return jsonify({'error': 'Invalid password. Please enter the correct password'}), 401
        
        token_identity = {'user_id': returned_user['user_id'], 'role': returned_user['role']}

        token = create_access_token(identity=token_identity, expires_delta=datetime.timedelta(hours=8))

        return jsonify({'message': '{} was successfully logged in'.format(email)}), 200
    except:
        return jsonify({'error': 'An error occured in trying to login the user'}), 501


@api.route("/api/v1/auth/signup", methods=["POST"])
@jwt_required
def register():
    """signs up a user"""
    try:
        logged_in_user = get_jwt_identity()

        if logged_in_user.get('role') == 'admin':
            json_data = request.get_json()

            email = json_data.get('email').strip()
            password = json_data.get('password').strip()

            email_status = Validator.validate_email(email)
            password_status = Validator.validate_password(password)

            if email_status is True:
                if password_status is True:
                    password_hash = generate_password_hash(password)

                    user = User(email, password_hash)
                    registration_status = user.register()

                    if not registration_status:
                        return jsonify({'error': 'User details could not be registered'}), 409

                    return jsonify({'message': registration_status}), 200

                return jsonify({'error': password_status}), 400

            return jsonify({'error': email_status}), 400
        return jsonify({'error': 'You are not authorized to access this endpoint'}), 401
    except:
        return jsonify({'error': 'There was an error in trying to register a user'}), 501

#PRODUCTS
#add new product
@api.route("/api/v1/products", methods=['POST'])
@jwt_required
def add_product():
    """adds new product"""
    try:
        logged_in_user = get_jwt_identity()
        if logged_in_user.get('role') == 'admin':
            json_data = request.get_json()

            name = json_data.get('name').strip()
            unit_price = json_data.get('unit_price')
            quantity = json_data.get('quantity')

            if name and unit_price and quantity:
                new_product = Product(name, unit_price, quantity)
                product_status = new_product.add_product()
                
                if not product_status:
                    return jsonify({'error': 'Product could not be added'}), 400

                return jsonify({'message': product_status}), 200

            return jsonify(product_status)
        return jsonify({'error': 'You are not authorized to access this endpoint'}), 401
    except:
        return jsonify({'error': 'There was an error in trying to add a product'}), 501

#get a single product
@api.route("/api/v1/products/<int:productId>", methods=['GET'])
@jwt_required
def get_a_product(productId):
    """returns a single product"""
    try:
        response = Product.get_single_product(productId)
        if not response:
            response = jsonify({'error': 'The are no products to fetch'})
        return jsonify(response), 400
    except:
        return jsonify({'error': 'There was an error in trying to fetch the product'}), 501

#get all product
@api.route("/api/v1/products", methods=['GET'])
@jwt_required
def get_all_products():
    """returns all products"""
    try:
        response = Product.get_all_products()

        if not response:
            response = jsonify({'error': 'There are no products to fetch'})
        return jsonify(response), 400
    except:
        return jsonify({'error': 'There was an error in trying to fetch products'}), 501

#get modify a product
@api.route("/api/v1/products/<productId>", methods=['PUT'])
@jwt_required
def modify_product(productId):
    """returns the modified product"""
    try:
        logged_in_user = get_jwt_identity()
        if logged_in_user.get('role') == 'admin':
            responses = []

            if not productId:
                responses.append({'error': 'You must specify the id for product to modify'}), 400

            json_data = request.get_json()

            if 'name' in json_data:
                return jsonify({'error': 'The product name cannot be modified'}), 400

            new_unit_price = json_data.get('unit_price')
            new_quantity = json_data.get('quantity')

            if new_unit_price:
                Product.modify_product(productId, 'unit_price', new_unit_price)

            if new_quantity:
                responses.append(Product.modify_product(productId, 'quantity', new_quantity))

            for response in responses:
                return jsonify(response)
        return jsonify({'error': 'You are not authorized to access this endpoint'}), 401
    except:
        return jsonify({'error': 'There was an error in trying to modify the product'}), 501

#delete a product
@api.route("/api/v1/products/<productId>", methods=['DELETE'])
@jwt_required
def delete_product(productId):
    """returns details of deleting a product """
    try:
        logged_in_user = get_jwt_identity()
        if logged_in_user.get('role') == 'admin':
            if not productId:
                response = {'error': 'You must specify the id for product to delete'}

            result = Product.delete_product(productId)
                
            return jsonify(result), 200
        return jsonify({'error': 'You are not authorized to access this endpoint'}), 400
    except:
        return jsonify({'error': 'There was an error in trying to delete the product'}), 500

#SALES
#add new sale
@api.route("/api/v1/sales", methods=['POST'])
@jwt_required
def add_sale():
    """adds new sale"""
    try:
        logged_in_user = get_jwt_identity()
        if logged_in_user.get('role') == 'attendant':
            quantity_in_db = 0
            product_to_update = 0
            product_to_update_id = 0 
            json_data = request.get_json()

            sale_product_name = json_data.get('name')
            sale_product_quantity = json_data.get('quantity')

            if not sale_product_name:
                return jsonify({'error': 'You need to provide a product name'})
            
            if not sale_product_quantity:
                return jsonify({'error': 'You need to provide a quantity for the product'})

            find_sale_product = Product.get_product_by_name(sale_product_name)

            if not find_sale_product:
                return jsonify({'error': 'Product does not exist. Please enter valid product name'})

            if find_sale_product:
                quantity_in_db = find_sale_product.get('quantity')

            if quantity_in_db == 0:
                return jsonify({'error': 'There are no products to sell'})

            if sale_product_quantity < 0:
                return jsonify({'error': 'Product quantity cannot be negative'})

            if sale_product_quantity > quantity_in_db:
                return jsonify({'error': 'There are less products stored than those you have requested for'})

            updated_quantity = quantity_in_db - sale_product_quantity
            product_to_update = Product.get_product_by_name(sale_product_name)

            if product_to_update:
                product_to_update_id = product_to_update.get('product_id')
                Product.modify_product(product_to_update_id, 'quantity', updated_quantity)

            if find_sale_product:
                total_sale_amount = sale_product_quantity * find_sale_product.get('unit_price')
        
            return jsonify({'Total Amount of Sale': total_sale_amount}), 200
        return jsonify({'error': 'You are not authorized to access this endpoint'}), 401
    except:
        return jsonify({'error': "There was an error in trying to add a new sale"}), 501

#get a single sale
# @api.route("/api/v1/sales/<int:saleId>", methods=['GET'])
# @jwt_required
# def get_a_sale(saleId):
#     """returns a single product"""
#     try:
#         if not Sale.all_sales:
#             return jsonify({'error':  'There are currently no sale records'})

#         for sale in Sale.all_sales:
#             if sale.get('sale_id') == saleId:
#                 return jsonify(sale), 200
        
#         return jsonify(response_object)
#     except:
#         response_object = {'error':  'Invalid request'}
#         return jsonify(response_object)

# #get all sales
# @api.route("/api/v1/sales", methods=['GET'])
# @jwt_required
# def get_all_sales():
#     """returns all sales"""
#     try:
#         if not Sale.all_sales:
#             return jsonify({'error':  'There are currently no sale records'})
#         return jsonify(Sale.all_sales)
#     except:
#         response_object = {'error':  'Invalid request'}
#         return jsonify(response_object)

#ERROR HANDLERS
@api.errorhandler(400)
def bad_request(error):
    """displays error msg when 400 error code is raised"""
    return jsonify({'message': 'A Bad request was sent to the server'}), 400

@api.errorhandler(404)
def record_not_found(error):
    """displays error msg when 404 error code is raised"""
    return jsonify({'message': 'Resource could not be found'}), 404

@api.errorhandler(401)
def unauthorized_access(error):
    """displays error message when 401 error code is raised"""
    return jsonify({'message': 'You are not authorized to access this resource'}), 401

@api.errorhandler(405)
def wrong_method(error):
    """displays error message when 405 error code is raised"""
    return jsonify({'message': 'You tried to access the resource using the wrong method.'}), 405