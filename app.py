from flask import Flask, render_template, request, json, jsonify
from api.resources.products.products import Product

api = Flask(__name__)

@api.route("/")
def index():
    """returns the index.html template"""
    role = request.args.get('role')

    if not role:
        role = "Visitor"

    return render_template('index.html', role=role)

#PRODUCTS
#add new product
@api.route("/api/v1/products", methods=['POST'])
def add_product():
    """adds new product"""
    try:
        json_data = request.get_json()

        if 'name' not in json_data:
            response_object = {'message': 'Request is missing the product name key'}
            return jsonify(response_object), 400

        if 'price' not in json_data:
            response_object = {'message': 'Request is missing the product price key'}
            return jsonify(response_object), 400

        if 'quantity' not in json_data:
            response_object = {'message': 'Request is missing the product quantity key'}
            return jsonify(response_object), 400

        if len(json_data.keys()) > 3:
            response_object = {'message': 'Request has more keys than expected'}
            return jsonify(response_object), 400

        if not isinstance(json_data.get('name'), str):
            response_object = {'message': 'Invalid data type for name value. Please enter a string'}
            return jsonify(response_object), 400

        if json_data.get('name') == '':
            response_object = {'message': 'The name of the product cannot be empty'}
            return jsonify(response_object), 400

        if not isinstance(json_data.get('price'), float):
            response_object = {'message': 'Invalid data type for price value. Please enter a float'}
            return jsonify(response_object), 400

        if json_data.get('price') == 0.00:
            response_object = {'message': 'The price of the product cannot be empty'}
            return jsonify(response_object), 400

        if not isinstance(json_data.get('quantity'), float):
            response_object = {'message': 'Invalid data type for quantity value. Please enter a float'}
            return jsonify(response_object), 400

        if json_data.get('quantity') == 0.00:
            response_object = {'message': 'The quantity of the product cannot be empty'}
            return jsonify(response_object), 400

        if json_data.get('price') <= 0.00:
            response_object = {'message':  'The price of the product cannot be zero or less than zero'}
            return jsonify(response_object), 400

        if json_data.get('quantity') <= 0.00:
            response_object = {'message':  'The quantity of the product cannot be zero or less than zero'}
            return jsonify(response_object), 400

        new_product = Product(json_data['name'], json_data['price'], json_data['quantity'])
        product_status = new_product.add_product()

        if product_status is True:
            added_product = Product.all_products[-1]
        return jsonify(added_product), 201
    except:
        response_object = {'message':  'Invalid request'}
        return jsonify(response_object)
    

#get a single product
@api.route("/api/v1/products/<int:productId>", methods=['GET'])
def get_a_product(productId):
    """returns a single product"""
    try:
        if not Product.all_products:
            return jsonify({'message':  'There are currently no product records'})

        for product in Product.all_products:
            if product.get('product_id') == productId:
                return jsonify(product), 200
        
        response_object = {'message':  'The product does not exist'}
        return jsonify(response_object)
    except:
        response_object = {'message':  'Invalid request'}
        return jsonify(response_object)

#get a ll products
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

@api.errorhandler(404)
def page_not_found(error):
    """displays page when 404 error code is raised"""
    return render_template('404.html'), 404

@api.errorhandler(401)
def unauthorized_access(error):
    """displays page when 401 error code is raised"""
    return render_template('401.html'), 401

@api.errorhandler(500)
def internal_server_error(error):
    """displays page when 500 error code is raised"""
    return render_template('500.html'), 500

@api.errorhandler(405)
def wrong_method(error):
    """displays page when 405 error code is raised"""
    return render_template('405.html'), 405

if __name__ == "__main__":
    api.run(debug=True)
