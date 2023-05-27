class Store:
    """
    The Store Class holds all of the products, and allows the user to make a
    purchase of multiple products at once.
    It contains one variable:  list of products that exist in the store.
    """

    def __init__(self, product_list: list):
        """
        The constructor method for the Store class. Creates the instance variables.
        Sets the instance parameter: product list that holds multiple products.
        :param product_list:
        """
        self._products = product_list

    def add_product(self, product: object):
        """
        Gets product and Adds product to store (product list)
        """
        self._products.append(product)
        return f"Product '{product}' successfully added to store"

    def remove_product(self, product: object):
        """
        Removes product from store ( product list)
        """
        self._products.remove(product)
        return f"Product '{product}' successfully removed from store"

    @property
    def total_quantity(self) -> int:
        """
        Returns how many items are in the store in total
        """
        total_quantity = 0
        for product in self._products:
            total_quantity += product.quantity
        return total_quantity

    @property
    def all_products(self):
        """
        Returns all products in the store that are active.
        """
        all_products = []
        for product in self._products:
            if product.is_active:
                all_products.append(product)
        return all_products

    def order(self, shopping_list):
        """
        Gets a list of tuples, where each tuple has 2 items:
        Product (Product object) and quantity (int).
        Buys the products.
        :returns: the total price of the order and total items received (as tuple)
        """
        total_order_price: float = 0
        total_item_received: int = 0
        for order in shopping_list:
            product, quantity = order
            # Total price of order per product
            total_price = product.buy(product, quantity)

            # if total price is tuple, then it has the buy 2, get 1 free promo
            if type(total_price) == tuple:
                total_price, total_item = total_price
                total_order_price += total_price
                total_item_received += total_item
            else:
                total_order_price += total_price
        return total_order_price, total_item_received

    def __contains__(self, item):
        return item in self._products

    def __add__(self, other):
        return Store(self._products + other._products)
