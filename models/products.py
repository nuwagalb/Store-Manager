from db_helper import DBHelper

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
        self.db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])

    def add_product(self):
        """add a product"""
        inserted_id = 0
        result = self.db.find_record(self.name)
        
        if not result:
            inserted_row = self.db.insert_record(
                    [self.name, self.unit_price, self.quantity, self.category_id]
                )
            inserted_id = inserted_row.get('product_id')
        
        if inserted_id:
            return self.db.find_record_by_id(inserted_id)

        return {}

    @staticmethod
    def get_single_product(product_id):
        """get a single product"""
        db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        product = db.find_record_by_id(product_id)

        if not product:
            return {}

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

        if find_record:
            deleted_product = db.delete_record(product_id)
            deleted_product_name = deleted_product.get('name')
            return deleted_product_name
        
        return ''

    @staticmethod
    def get_product_by_name(product_name):
        """"gets a product by it's name"""
        db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        found_product = db.find_record(product_name)

        return found_product
        
