class Product:
    """Class that handles all the actions that can be performed
       on a Product such as: creating a new product, viewing details 
       of a product, updating a product's details and deleting a product
    """
    all_products = []

    def __init__(self, name="", price=0.00, quantity=0.00):
        """Initializes the Product class"""
        (self.name, self.price, self.quantity) = (name, price, quantity)

    def add_product(self):
        """adds product record to """
        if not Product.all_products:
            product_id = 1
        else:
            product_id = Product.all_products[-1].get('product_id') + 1

        Product.all_products.append(
            {'product_id': product_id, 'name': self.name, 'price': self.price, 'quantity': self.quantity}
        )

        return True

    def get_single_product(self, product_id):
        """returns a single product """
        product = [product for product in Product.all_products if product.get('product_id') == product_id]

        return product[0]
        