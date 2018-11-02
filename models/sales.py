from db_helper import DBHelper
class Sale:
    """Class that handles all the actions that can be performed
       on a Sale such as: creating a new sale, viewing details 
       of a sale, updating a sale's details and deleting a sale
    """
    def __init__(self, sales_order_no, total_amount, user_id):
        self.sales_order_no = sales_order_no
        self.total_amount = total_amount
        self.user_id = user_id       

    def add_sale(self):
        """add a sale"""
        db = DBHelper('sales', ['sales_id', 'sales_order_no', 'total_amount', 'user_id'])
        result = db.find_record(self.sales_order_no)

        if not result:
            db.insert_record([self.sales_order_no, self.total_amount, self.user_id])
            return db.find_record(self.sales_order_no)
        return "There already exists a sale with that name"

    @staticmethod
    def get_single_sale(sale_id):
        """get a single sale"""
        db = DBHelper('sales', ['sales_id', 'sales_order_no', 'total_amount', 'user_id'])
        sale = db.find_record_by_id(sale_id)

        if not sale:
            return {'message': 'The record you are searching for was not found'}
        return sale

    @staticmethod
    def get_all_sales():
        """get all available sales"""
        db = DBHelper('sales', ['sale_id', 'sale_order_no', 'total_amount', 'user_id'])
        results = db.find_all_records()
        
        return results
        