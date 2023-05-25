class Product:
    """
    The Product class represents a specific type of product available in the store
    (For example, MacBook Air M2).
    It encapsulates information about the product, including its name and price.
    It includes an attribute to keep track of the total quantity of items of that
    product currently available in the store. When someone will purchase it,
    the amount will be modified accordingly.
    """
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
        elif quantity <= 0:
            raise ValueError("The argument: 'quantity' must be greater than 0")

        self._product_name = name
        self._price = price
        self._quantity = quantity
        self._active = True

    def get_quantity(self) -> float:
        """
        Getter function for quantity. Returns the quantity (float).
        :return: quantity (float)
        """
        return self._quantity

    def set_quantity(self, quantity: int):
        """
        Setter function for quantity. If quantity reaches 0, deactivates the product.
        :param quantity:
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
        "MacBook Air M2, Price: 1450, Quantity: 100"
        """
        product = f"{self._product_name}, Price: {self._price}, Quantity: {self._quantity}"
        return product

    def buy(self, quantity: int) -> float:
        """
        Gets a given quantity of the product.
        Returns the total price (float) of the purchase.
        Updates the quantity of the product.
        """
        if isinstance(quantity, str):
            raise ValueError("Quantity must be an integer")
        if quantity <= 0:
            raise ValueError("Quantity must be greater than 0")
        if quantity > self._quantity:
            raise ValueError(f"The quantity {quantity} entered is above the quantity of "
                             "product in the store")

        total_price = self._price * quantity
        self._quantity -= quantity
        return total_price