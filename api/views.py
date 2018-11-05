from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models.products import Product
from models.sales import Sale
from models.users import User
from models.validators import Validator
import datetime
from db_helper import DBHelper
import os

api = Flask(__name__)

api.config['JWT_SECRET_KEY'] = '89#456612dfmrprkp'

os.environ['DATABASE_URL'] = 'postgres://ayismiynoayaqa:4aa137351e4c1da6449f \
                             aa235879ca0f8d4403311c4638e11b79f89963329ac4@ec2- \
                             184-73-169-151.compute-1.amazonaws.com:5432/d52fe7v\
                             tm6hiqf'

jwt = JWTManager(api)

@api.route("/api/v2/auth/login", methods=["POST"])
def login():
    """logs in a user"""
    try:
        password_status = False
        json_data = request.get_json()
        email = json_data.get('email').strip()
        password = json_data.get('password').strip()

        user = User(email, password)

        returned_user = user.get_record(email)
        current_password = user.get_record(email)

        if not returned_user:
            return jsonify({'error': 'Invalid email address. Please enter the correct email'}), 404

        if current_password:
            password_status = check_password_hash(current_password.get('password'), password)

        if not password_status:
            return jsonify({'error': 'Invalid password. Please enter the correct password'}), 404

        if password_status:
            token_identity = {'user_id': returned_user['user_id'], 'role': returned_user['role']}
            token = create_access_token(identity=token_identity, expires_delta=datetime.timedelta(hours=8))

        return jsonify({'token': token, 'message': '{} was successfully logged in'.format(email)}), 200
    except:
        return jsonify({'error': 'An error occured in trying to login the user'}), 400


@api.route("/api/v2/auth/signup", methods=["POST"])
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
                        return jsonify({'error': 'Email address already exists. Please provide a different email'
                                       }), 409

                    return jsonify(registration_status), 201

                return jsonify({'error': password_status}), 400

            return jsonify({'error': email_status}), 400
        return jsonify({'error': 'Access to this resource is forbidden'}), 403
    except:
        return jsonify({'error': 'There was an error in trying to register the user'}), 400

#PRODUCTS
#add new product
@api.route("/api/v2/products", methods=['POST'])
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
                    return jsonify({'error': 'Product already exists. Please select a different name'
                                   }), 409

                return jsonify(product_status), 201

            return jsonify(product_status)
        return jsonify({'error': 'Access to this resource is forbidden'}), 403
    except:
        return jsonify({'error': 'There was an error in trying to add a product'}), 400

#get a single product
@api.route("/api/v2/products/<int:productId>", methods=['GET'])
@jwt_required
def get_a_product(productId):
    """returns a single product"""
    product_status = Product.get_single_product(productId)

    if not product_status:
        return jsonify({'error': 'Invalid request. The product you are searching for does not exist'}), 404
        
    return jsonify(product_status), 200

#get all product
@api.route("/api/v2/products", methods=['GET'])
@jwt_required
def get_all_products():
    """returns all products"""
    product_status = Product.get_all_products()

    if not product_status:
        return jsonify({'error': 'There are no products to fetch'}), 404

    return jsonify(product_status), 200

#get modify a product
@api.route("/api/v2/products/<productId>", methods=['PUT'])
@jwt_required
def modify_product(productId):
    """returns the modified product"""
    logged_in_user = get_jwt_identity()
    if logged_in_user.get('role') == 'admin':
        
        json_data = request.get_json()

        new_name = json_data.get('name')
        new_unit_price = json_data.get('unit_price')
        new_quantity = json_data.get('quantity')

        if new_name:
            Product.modify_product(productId, 'name', new_name)

        if new_unit_price:
            Product.modify_product(productId, 'unit_price', new_unit_price)

        if new_quantity:
            Product.modify_product(productId, 'quantity', new_quantity)

        modified_product = Product.get_single_product(productId)

        if not modified_product:
            return jsonify({'error': 'The product you tried to modify does not exsit.'}), 404

        return jsonify(modified_product), 200

    return jsonify({'error': 'Access to this resource is forbidden'}), 403

#delete a product
@api.route("/api/v2/products/<productId>", methods=['DELETE'])
@jwt_required
def delete_product(productId):
    """returns details of deleting a product """
    logged_in_user = get_jwt_identity()
    if logged_in_user.get('role') == 'admin':

        deleted_product = Product.delete_product(productId)

        if not deleted_product:
            return jsonify({'error': 'The product you tried to delete does not exist'}), 404
            
        return jsonify({'message': '{} was successfully deleted'.format(deleted_product)}), 200

    return jsonify({'error': 'Access to this resource is forbidden'}), 403

#SALES
#add new sale
@api.route("/api/v2/sales", methods=['POST'])
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

            sale_product_id = json_data.get('product_id')
            sale_product_quantity = json_data.get('quantity')

            if not sale_product_id:
                return jsonify({'error': 'You need to provide a product id'}), 400
            
            if not sale_product_quantity:
                return jsonify({'error': 'You need to provide a quantity for the product'}), 400

            if sale_product_quantity < 0:
                return jsonify({'error': 'Product quantity cannot be negative'}), 400

            found_sale_product = Product.get_single_product(sale_product_id)

            if not found_sale_product:
                return jsonify({'error': 'Product does not exist. Please enter valid product id'}), 404

            quantity_in_db = found_sale_product.get('quantity')

            if quantity_in_db == 0:
                return jsonify({'error': 'There are no products to sell'}), 404

            if sale_product_quantity > quantity_in_db:
                return jsonify({'error': 'The quantity you requested for is more than that in stock'}), 404

            updated_quantity = quantity_in_db - sale_product_quantity
            product_to_update = Product.get_single_product(sale_product_id)

            if product_to_update:
                product_to_update_id = product_to_update.get('product_id')
                Product.modify_product(product_to_update_id, 'quantity', updated_quantity)

            total_sale_amount = sale_product_quantity * found_sale_product.get('unit_price')

            new_sale = Sale(product_to_update_id, sale_product_quantity,
                            total_sale_amount, logged_in_user.get('user_id'))

            sale_order_id = new_sale.add_sale()

            if not sale_order_id:
                return jsonify({'error': 'Sale order could not be created'}), 400

            return jsonify({'Product id': product_to_update_id,
                            'Total Amount of Sale': total_sale_amount,
                            'Quantity sold': sale_product_quantity, 
                            'Quantity left in stock': updated_quantity
                            }), 201
        return jsonify({'error': 'Access to this resource is forbidden'}), 403
    except:
        return jsonify({'error': 'There was an error in trying to add a new sale'}), 400

#get a single sale
@api.route("/api/v2/sales/<int:saleId>", methods=['GET'])
@jwt_required
def get_a_sale(saleId):
    """returns a single product"""
    result = Sale.get_single_sale(saleId)

    if not result:
        return jsonify({'error': 'The sale you are trying to fetch does not exist'}), 404

    return jsonify(result), 200

#get all sales
@api.route("/api/v2/sales", methods=['GET'])
@jwt_required
def get_all_sales():
    """returns all sales"""
    results = Sale.get_all_sales()

    if not results:
        return jsonify({'error': 'There are no sales to fetch'}), 404

    return jsonify(results), 200

#ERROR HANDLERS
@api.errorhandler(400)
def bad_request(error):
    """displays error msg when 400 error code is raised"""
    return jsonify({'message': 'A Bad request was sent to the server'}), 400

@api.errorhandler(404)
def record_not_found(error):
    """displays error msg when 404 error code is raised"""
    return jsonify({'message': 'Resource could not be found'}), 404

@api.errorhandler(403)
def unauthorized_access(error):
    """displays error message when 403 error code is raised"""
    return jsonify({'message': 'You are not authorized to access this resource'}), 403

@api.errorhandler(405)
def wrong_method(error):
    """displays error message when 405 error code is raised"""
    return jsonify({'message': 'You tried to access the resource using the wrong method.'}), 405