from db_helper import DBHelper
import json

class Product:
    """Class that handles all the actions that can be performed
       on a Product such as: creating a new product, viewing details
       of a product, updating a product's details and deleting a product
    """

    def __init__(self, name, unit_price, quantity, category_id=0):
        self.name = name
        self.unit_price = unit_price
        self.quantity = quantity
        self.category_id = category_id

    def add_product(self):
        """add a product"""
        db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        result = db.find_record(self.name)

        if not result:
            return db.insert_record([self.name, self.unit_price, self.quantity])
        return "There already exists a product with that name"

    @staticmethod
    def get_single_product(product_id):
        """get a single product"""
        db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        product = db.find_record_by_id(product_id)

        if not product:
            return {'message': 'The record you are searching for was not found'}
        return product

    @staticmethod
    def get_all_products():
        """get all available products"""
        db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        results = db.find_all_records()
        
        return results

    @staticmethod
    def modify_product(product_id, field_name, value):
        """modify product details"""
        db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        
        return db.update_record(field_name, value, 'product_id', product_id)

    @staticmethod
    def delete_product(product_id):
        """deletes a product"""
        db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        find_record = db.find_record_by_id(product_id)

        if not find_record:
            return {'message': 'The record your trying to delete does not exist'}
        
        return db.delete_record(product_id)

    @staticmethod
    def get_product_by_name(product_name):
        """"gets a product by it's name"""
        db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        find_product = db.find_record(product_name)

        return find_product


