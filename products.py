class Product:
    """
    The Product class represents a specific type of product available in the store
    (For example, MacBook Air M2).
    It encapsulates information about the product, including its name and price.
    It includes an attribute to keep track of the total quantity of items of that
    product currently available in the store. When someone will purchase it,
    the amount will be modified accordingly.
    """
    promotion = object()

    def __init__(self, name: str, price: float, quantity: int):
        """
        Initiator (constructor) method. Creates the instance variables (active is set
        to True). If something is invalid (empty name / negative price or quantity),
        raises an exception.
        """

        if not name:
            raise NameError("The argument: 'name' cannot be empty")
        if isinstance(name, int):
            raise NameError("The argument: 'name' must be a string")
        else:
            if name.isdigit():
                raise NameError("The argument: 'name' must be string")
        if isinstance(price, str):
            raise ValueError("The argument: 'price' must be a number")
        elif price <= 0:
            raise ValueError("The argument: 'price' must be greater than 0")
        if isinstance(quantity, str):
            raise ValueError("The argument: 'price' must be an integer")
        elif quantity < 0:
            raise ValueError("The argument: 'quantity' must be greater than 0")

        self._product_name = name
        self._price = price
        self._quantity = quantity
        self._active = True
        self._non_stocked_product = False
        self._total_price = 0

    def get_price(self) -> float:
        """ Getter function for price. Returns the price (float) """
        return self._price

    def set_price(self, new_price):
        """ Setter function for price. """
        self._price = new_price

    def get_total_price(self) -> float:
        """ Getter function for total price. Returns the total price (float) """
        return self._total_price

    def set_total_price(self, new_total_price):
        """ Setter function for total price. """
        self._total_price = new_total_price

    def get_promotion(self):
        """ Getter function for the promotion object (class variable).
        Returns the promotion object"""
        return self.promotion

    def set_promotion(self, promotion_obj: object):
        """
         Setter function for the promotion object (class variable).
        """
        self.promotion = promotion_obj

    def is_non_stocked_product(self):
        """
        Getter function for Non Stocked Product. Quantity of Non Stocked Product is
        always  zero.
        Returns True if it is Non Stocked Product, otherwise False.
        """
        return self._non_stocked_product

    def get_quantity(self) -> float:
        """
        Getter function for quantity. Returns the quantity (float).
        :return: quantity (float)
        """
        return self._quantity

    def set_quantity(self, quantity: int):
        """
        Setter function for quantity. If quantity reaches 0, deactivates the product.
        """
        if isinstance(quantity, str):
            raise ValueError("The argument: 'quantity' must be an integer")
        self._quantity += quantity

        # Deactivates product if product quantity is 0 (i.e., it is out of stock)
        if self.get_quantity() <= 0:
            self._quantity = 0
            self.deactivate()

    def is_active(self) -> bool:
        """
        Getter function for active.
        Returns True if the product is active, otherwise False.
        :return: True or False (bool)
        """
        if self.get_quantity() <= 0:
            self._active = False
        return self._active

    def activate(self):
        """
        Activates the product.
        """
        self._active = True
        self._product_name = self._product_name.removesuffix(' (deactivated)').strip()

    def deactivate(self):
        """
        Deactivates the product
        """
        self._active = False
        self._product_name += ' (deactivated)'

    def show(self) -> str:
        """
        Returns a string that represents the product, for example:
        "MacBook Air M2, Price: 1450, Quantity: 100, Promotion: 30% off"
        if Promotion is not available on the product, Promotion: None
        """
        if self.is_active():
            try:
                return f"{self._product_name}, Price: {self._price}, " \
                       f"Quantity: {self._quantity}, Promotion: {self.promotion.get_name()}"
            except AttributeError:
                # if there is no promotion
                return f"{self._product_name}, Price: {self._price}, " \
                       f"Quantity: {self._quantity}, Promotion: None"

    def buy(self, product: object, quantity: int) -> float:
        """
        Gets a product object and given quantity of the product.
        If promotion is set on the product, it applies promotion on the product.
        Returns the total price (float) of the purchase or the discounted price
        Updates the quantity of the product.
        """
        if isinstance(quantity, str) or isinstance(quantity, float):
            raise ValueError("Quantity must be an integer")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if quantity > self._quantity:
            raise ValueError(f"The quantity {quantity} entered is above the quantity of "
                             "product in the store")

        # Gets the total price for the product [price * quantity]
        self._total_price = self.get_price() * quantity
        # check if there is promotion for the product
        if type(self.promotion) != object:
            discount_price = product.get_promotion().apply_promotion(product, quantity)
            self._quantity -= quantity
            return discount_price
        else:
            self._quantity -= quantity
            return self._total_price


class NonStockedProduct(Product):
    """
    Some products in the store are not physical, so we don’t need to keep track
    of their quantity. for example - a Microsoft Windows license.
    On these products, the quantity is always set to zero and stays that way.
    """

    def __init__(self, name: str, price: float):
        """ Initiator (constructor) method. Creates the instance variables for
        NonStockedProduct class  """
        super().__init__(name, price, quantity=0)
        self._name = name
        self._price = price
        self._quantity = 0
        self._non_stocked_product = True

    def is_active(self) -> bool:
        """
        Getter function for active.
        Returns True if the product is active, otherwise False.
        The Non Stocked Product is always active
        """
        return self._active

    def is_non_stocked_product(self):
        """
        Getter function for Non Stocked Product.
        Quantity of Non Stocked Product is always  zero.
        Returns True if it is Non Stocked Product, otherwise False.
        """
        return self._non_stocked_product

    def show(self) -> str:
        """
        Returns a string that represents the product, for example:
        "MacBook Air M2, Price: 1450, Quantity: 100, Promotion: Second Half Price"
        if Promotion is not available on the product, Promotion: None
        """
        try:
            product = f"{self._product_name}, Price: {self._price}, Quantity: Unlimited, " \
                      f"Promotion: {self.promotion.get_name()}"
        except AttributeError:
            product = f"{self._product_name}, Price: {self._price}, Quantity: Unlimited, " \
                      f"Promotion: None"
        return product

    def buy(self, product: object, quantity: int) -> float:
        """
        Gets a product object and given quantity of the product.
        If promotion is set on the product, it applies promotion on the product.
        Returns the total price (float) of the purchase or the discounted price
        Updates the quantity of the product.
        Quantity in store for Non Stocked Product is unlimited (always zero)
        """
        if isinstance(quantity, str) or isinstance(quantity, float):
            raise ValueError("Quantity must be an integer")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")

        # Gets the total price for the product [price * quantity]
        self._total_price = self._price * quantity

        # check if there is promotion for the product
        if type(self.promotion) != object:
            discount_price = product.get_promotion().apply_promotion(product, quantity)
            return discount_price

        return self._total_price


class LimitedProduct(Product):
    """
    Some products quantity can only be a maximum of X- number in a single order.
    If an order is attempted with quantity larger than the maximum X- number, it
    refuses with an exception.
    """
    def __init__(self, name: str, price: float, quantity: int, maximum: int):
        """ Constructor method. Creates the instance variables for LimitedProduct Class """
        super().__init__(name, price, quantity)
        self._product_name = name
        self._price = price
        self._quantity = quantity
        self._max_purchase = maximum

    def show(self) -> str:
        """
        Returns a string that represents the product, for example:
        "MacBook Air M2, Price: 1450, Quantity: 100, Promotion: Second Half Price"
        if Promotion is not available on the product, Promotion: None
        """
        try:
            product = f"{self._product_name}, Price: {self._price}, " \
                      f"Limited to {self._max_purchase} per order!, " \
                      f"Promotion: {self.promotion.get_name()}"
        except AttributeError:
            product = f"{self._product_name}, Price: {self._price}, " \
                      f"Limited to {self._max_purchase} per order!, " \
                      f"Promotion: None"
        return product

    def buy(self, product: object, quantity: int) -> float:
        """
        Gets a product object and given quantity of the product.
        If promotion is set on the product, it applies promotion on the product.
        Returns the total price (float) of the purchase or the discounted price
        Updates the quantity of the product.
        """
        if isinstance(quantity, str) or isinstance(quantity, float):
            raise ValueError("Quantity must be an integer")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if quantity > self._max_purchase:
            raise ValueError(f"Error: Only maximum quantity of {self._max_purchase} per "
                             "order is allowed!")

        # Gets the total price for the product [price * quantity]
        self._total_price = self._price * quantity

        # check if there is promotion for the product
        if type(self.promotion) != object:
            discount_price = product.get_promotion().apply_promotion(product, quantity)
            return discount_price
        return self._total_price


# setup initial stock of inventory
product_list = [Product("MacBook Air M2", price=1450, quantity=100),
                Product("Bose QuietComfort Earbuds", price=250, quantity=500),
                Product("Google Pixel 7", price=500, quantity=250),
                NonStockedProduct("Windows License", price=125),
                LimitedProduct("Shipping", price=10, quantity=250, maximum=1)
                ]