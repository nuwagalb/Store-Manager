class Sale:
    """Class that handles all the actions that can be performed
       on a Sale such as: creating a new sale, viewing details 
       of a sale, updating a sale's details and deleting a sale
    """
    all_sales = []

    def __init__(self, product_id=0, quantity=0.00, amount=0.00):
        """Initializes the Sale class"""
        (self.product_id, self.quantity, self.amount) = (product_id, quantity, amount)

    def add_sale(self):
        """adds sale record to """
        if not Sale.all_sales:
            sale_id = 1
        else:
            sale_id = Sale.all_sales[-1].get('sale_id') + 1

        Sale.all_sales.append(
            {'sale_id': sale_id, 'product_id': self.product_id, 'quantity': self.quantity, 'amount': self.amount}
        )

        return True

    def get_single_sale(self, sale_id):
        """returns a single sale """
        sale = [sale for sale in Sale.all_sales if sale.get('sale_id') == sale_id]

        return sale[0]
        