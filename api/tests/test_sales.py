import unittest
from ..resources.sales.sales import Sale

class SaleTestCase(unittest.TestCase):
    """
        class contains tests for all the methods and attributes
        of the Sale Class
    """
    def setUp(self):
        self.sale = Sale(1, "18-10-18", 2000.00)
        self.sale_record = {'sale_id': 1, 'product_id_id': 'Samsung Galaxy A9', 'date': 239.98, 'amount': 2.00}

    def test_proper_initialization_of_the_sales_class(self):
        """tests for proper initialization of the sale class"""
        self.assertIsInstance(self.sale.all_sales, list)
        self.assertIsInstance(self.sale.product_id, int)
        self.assertIsInstance(self.sale.quantity, str)
        self.assertIsInstance(self.sale.amount, float)

    def test_add_sale_method_returns_true_when_new_sale_is_added_to_the_list(self):
        """test that sale record is successfully saved"""
        self.assertEqual(self.sale.add_sale(), True)
        
        