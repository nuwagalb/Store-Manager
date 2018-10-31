from db_helper import DBHelper


class Product:
    """Class that handles all the actions that can be performed
       on a Product such as: creating a new product, viewing details
       of a product, updating a product's details and deleting a product
    """
    all_products = []

    def __init__(self, name, unit_price, quantity, category_id=0):
        self.name = name
        self.unit_price = unit_price
        self.quantity = quantity
        self.category_id = category_id

    def add_product(self):
        """add a product"""
        db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        insertion_status = db.insert_record([
                        self.name,
                        self.unit_price,
                        self.quantity
                    ])
        return insertion_status

    def get_single_product(self, product_id):
        """get a single product"""
        self.product_id = product_id
        db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
        product = db.find_record_by_id(self.product_id)