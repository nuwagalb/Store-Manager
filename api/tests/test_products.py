import unittest
from ..resources.products.products import Product

class ProductTestCase(unittest.TestCase):
    """
        class contains tests for all the methods and attributes
        of the Product Class
    """
    def setUp(self):
        self.product = Product('Samsung Galaxy A9', 239.98, 2.00)
        self.product_record = {'product_id': 1, 'name': 'Samsung Galaxy A9', 'price': 239.98, 'quantity': 2.00}

    def test_proper_initialization_of_the_products_class(self):
        """tests for proper initialization of the product class"""
        self.assertIsInstance(self.product.all_products, list)
        self.assertIsInstance(self.product.name, str)
        self.assertIsInstance(self.product.price, float)
        self.assertIsInstance(self.product.quantity, float)

    def test_add_product_method_returns_true_when_new_product_is_added_to_the_list(self):
        """test that product record is successfully saved"""
        self.assertEqual(self.product.add_product(), True)
        
        