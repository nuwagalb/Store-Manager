from db_helper import DBHelper

class Sale:
    """Class that handles all the actions that can be performed
       on a Sale such as: creating a new sale, viewing details 
       of a sale, updating a sale's details and deleting a sale
    """
    def __init__(self, product_id, quantity, total_amount, user_id):
        self.product_id = product_id
        self.quantity = quantity
        self.total_amount = total_amount
        self.user_id = user_id        

    def add_sale(self):
        """add a sale"""
        db = DBHelper(
                'sales', 
                ['sale_id', 'product_id', 'quantity',
                 'total_amount', 'user_id'
                ]
            )

        new_sale = db.insert_record([self.product_id, self.quantity,
                                    self.total_amount, self.user_id])
        if new_sale:
            return new_sale.get('sale_id')

        return 0

    @staticmethod
    def get_single_sale(sale_id):
        """get a single sale"""
        db = DBHelper('sales', ['sale_id', 'product_id', 'quantity', 'total_amount', 'user_id'])
        sale = db.find_record_by_id(sale_id)

        if not sale:
            return {}

        return sale

    @staticmethod
    def get_all_sales():
        """get all available sales"""
        db = DBHelper('sales', ['sale_id', 'product_id', 'quantity', 'total_amount', 'user_id'])
        sales = db.find_all_records()
        
        return sales

    @staticmethod
    def get_sales_by_user(user_id):
        """gets all available sales by a given user"""
        db = DBHelper('sales', ['sale_id', 'product_id', 'quantity', 'total_amount', 'user_id'])
        sales = db.find_all_user_records(user_id)

        if not sales:
            return []

        return sales

        
        