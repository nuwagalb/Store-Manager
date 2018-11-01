from db_helper import DBHelper
class Sale:
    """Class that handles all the actions that can be performed
       on a Sale such as: creating a new sale, viewing details 
       of a sale, updating a sale's details and deleting a sale
    """
    def __init__(self, total_amount, user_id):
        self.total_amount = total_amount
        self.user_id = user_id
        

    # def add_sale(self):
    #     """add a sale"""
    #     db = DBHelper('sales', ['sales_id', 'total_amount', 'user_id'])
    #     result = db.find_record(self.)

    #     if not result:
    #         return db.insert_record([self.name, self.unit_price, self.quantity])
    #     return "There already exists a product with that name"

    # @staticmethod
    # def get_single_product(product_id):
    #     """get a single product"""
    #     db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
    #     product = db.find_record_by_id(product_id)

    #     if not product:
    #         return {'message': 'The record you are searching for was not found'}
    #     return product

    # @staticmethod
    # def get_all_products():
    #     """get all available products"""
    #     db = DBHelper('products', ['product_id', 'name', 'unit_price', 'quantity'])
    #     results = db.find_all_records()
        
    #     return results
        