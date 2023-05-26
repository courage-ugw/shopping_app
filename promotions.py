import math
from abc import ABC, abstractmethod


class Promotion(ABC):
    """
    The Promotion Class is an Abstract Class that applies discounts and promotions to
    certain  products. The promotions that extend the Promotion Class implements the
     abstract method. For example:
        Percentage discount (i.e. 20% off)
        Second item at half price
        Buy 2, get 1 free
    """

    def __init__(self, name):
        """ Constructor of the Promotion Class"""
        self._name = name

    def get_name(self):
        """ Getter method for the name attribute"""
        return self._name

    def set_name(self, new_name):
        """ Setter method for the name attribute"""
        self._name = new_name

    @abstractmethod
    def apply_promotion(self, product, quantity) -> float:
        """
        Abstract Method. To be overwritten and implemented by Promotion subclasses.
        Gets product object, and order quantity and returns the discounted price after
        promotion has been applied to product price.
        :param product: product instance
        :param quantity: order quantity
        :return: discount price (float)
        """
        pass


class PercentDiscount(Promotion):
    """
    Gets name of promotion and percent to be discounted
    """
    def __init__(self, name: str, percent: int):
        """ constructor for the PercentDiscount subclass"""
        super().__init__(name)
        self._percent = percent

    def apply_promotion(self, product, quantity) -> float:
        """
        Gets product object, and order quantity and returns the discounted price after
        promotion has been applied to product price.
        :param product: product instance
        :param quantity: order quantity
        :return: discount price (float)
        """
        total_price = product.get_total_price()
        discount_price = total_price - (total_price * self._percent * 0.01)
        return discount_price


class SecondHalfPrice(Promotion):
    """ Gets the name of the promotion: Second at Half Price. Applies promotion on
     the product"""
    def __init__(self, name):
        """ constructor for the SecondHalfPrice subclass"""
        super().__init__(name)
        self.name = name

    def apply_promotion(self, product, quantity) -> float:
        """
        Gets product object, and order quantity and returns the discounted price after
        promotion has been applied to product price.
        :param product: product instance
        :param quantity: order quantity
        :return: discount price (float)
        """
        regular_price = product.get_price()
        full_priced_items = quantity - math.floor(quantity / 2)
        half_priced_items = math.floor(quantity / 2)
        half_of_regular_price = regular_price / 2
        discount_price = (full_priced_items * regular_price) + \
                         (half_priced_items * half_of_regular_price)
        return discount_price


class ThirdOneFree(Promotion):
    """ Gets the name of promotion: Buy 2, Get 1 Free. Apply promotion on product """
    def __init__(self, name):
        """ constructor for the ThirdOneFree subclass"""
        super().__init__(name)
        self.name = name

    def apply_promotion(self, product, quantity) -> tuple:
        """
        Gets product object, and order quantity and returns the discounted price after
        promotion has been applied to product price.
        :param product: product instance
        :param quantity: order quantity
        :return: price and total item received (tuple)
        """
        price = product.get_price()
        total_price = price * quantity
        total_item_received = quantity + (quantity // 2)
        return total_price, total_item_received
