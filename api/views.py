from flask import Flask, render_template, request, jsonify
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models.products import Product
from models.sales import Sale
from models.users import User
from os import environ

api = Flask(__name__)

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
    email_status = user.get_email(email)
    password_status = user.get_password(password)

    if not email_status:
       return jsonify({'message': 'Invalid email address. Please enter the correct email address'})
    
    if check_password_hash(password_status, password):
        token = create_access_token(identity=password_status.get('role'))
        return jsonify({'token': token, 'message': '{} was successfully logged in'.format(email)})
        
    return jsonify({'message': 'Invalid password. Please enter the correct password'})

#PRODUCTS
#add new product
@api.route("/api/v1/products", methods=['POST'])
def add_product():
    """adds new product"""
    json_data = request.get_json()

    try:
        if 'name' not in json_data:
            response_object = {'message': 'Request is missing the product name key'}
            status_code = 400

        elif 'price' not in json_data:
            response_object = {'message': 'Request is missing the product price key'}
            status_code = 400

        elif 'quantity' not in json_data:
            response_object = {'message': 'Request is missing the product quantity key'}
            status_code = 400

        elif len(json_data.keys()) > 3:
            response_object = {'message': 'Request has more keys than expected'}
            status_code = 400

        elif not isinstance(json_data.get('name'), str):
            response_object = {'message': 'Invalid data type for name value. Please enter a string'}
            status_code = 400

        elif json_data.get('name') == '':
            response_object = {'message': 'The name of the product cannot be empty'}
            status_code = 400

        elif not isinstance(json_data.get('price'), float):
            response_object = {'message': 'Invalid data type for price value. Please enter a float'}
            status_code = 400

        elif json_data.get('price') == 0.00:
            response_object = {'message': 'The price of the product cannot be empty'}
            status_code = 400

        elif not isinstance(json_data.get('quantity'), float):
            response_object = {'message': 'Invalid data type for quantity value. Please enter a float'}
            status_code = 400

        elif json_data.get('quantity') == 0.00:
            response_object = {'message': 'The quantity of the product cannot be empty'}
            status_code = 400

        elif json_data.get('price') <= 0.00:
            response_object = {'message':  'The price of the product cannot be zero or less than zero'}
            status_code = 400

        elif json_data.get('quantity') <= 0.00:
            response_object = {'message':  'The quantity of the product cannot be zero or less than zero'}
            status_code = 400

        else:
            new_product = Product(json_data['name'], json_data['price'], json_data['quantity'])

            if new_product.add_product() is True:
                added_product = Product.all_products[-1]
                response_object = added_product
                status_code = 201
                            
        return jsonify(response_object), status_code
    except:
        return jsonify({'message':  'Invalid product request'})
    

#get a single product
@api.route("/api/v1/products/<int:productId>", methods=['GET'])
def get_a_product(productId):
    """returns a single product"""
    try:
        if not Product.all_products:
            response_object = {'message':  'There are currently no product records'}
        else:
            for product in Product.all_products:
                if product.get('product_id') == productId:
                    response_object = product
                    status_code = 200
        return jsonify(response_object), status_code
    except:
        return jsonify({'message':  'Invalid request'})

#get all products
@api.route("/api/v1/products", methods=['GET'])
def get_all_products():
    """returns all products"""
    try:
        if not Product.all_products:
            return jsonify({'message':  'There are currently no product records'})
        return jsonify(Product.all_products)
    except:
        response_object = {'message':  'Invalid request'}
        return jsonify(response_object)

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

#GENERAL PURPOSE FUNCTIONS



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