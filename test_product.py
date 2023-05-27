import pytest
from products import Product


def test_creating_products():
    """
    Test that creating a normal product works.
    """
    mac_book = Product("MacBook Air M2", price=1450, quantity=100)
    assert isinstance(mac_book, Product)


def test_creating_product_invalid_name():
    """
    Test that creating a product with invalid name or empty name
    invokes an exception
    """
    with pytest.raises(NameError):
        Product(" ", price=140, quantity=100)
        Product("45", price=140, quantity=100)


def test_creating_product_negative_or_zero_price():
    """
    Test that creating a product with negative price or 0 price
    invokes an exception
    """
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=-150, quantity=100)
        Product("MacBook Air M2", price=0, quantity=100)


def test_creating_product_negative_or_zero_quantity():
    """
    Test that creating a product with negative price or 0 quantity
    invokes an exception
    """
    with pytest.raises(ValueError):
        Product("MacBook Air M2", price=100, quantity=-100)


def test_product_becomes_inactive():
    """
    Test that when a product reaches 0 quantity, it becomes inactive.
    """
    mac_book = Product("MacBook Air M2", price=1450, quantity=100)
    mac_book.quantity = -100
    assert not mac_book.is_active


def test_buy_modifies_quantity():
    """
    Test that product purchase modifies the quantity and returns the right output
    """
    mac_book = Product("MacBook Air M2", price=1450, quantity=100)
    mac_book.buy(mac_book, 40)
    assert mac_book.quantity == 60


def test_buy_too_much():
    """
    Test that buying a larger quantity than exists invokes exception.
    """
    with pytest.raises(ValueError):
        mac_book = Product("MacBook Air M2", price=1450, quantity=100)
        mac_book.buy(mac_book, 400)



"""
# setup initial stock of inventory
mac =  products.Product("MacBook Air M2", price=1450, quantity=100)
bose = products.Product("Bose QuietComfort Earbuds", price=250, quantity=500)
pixel = products.LimitedProduct("Google Pixel 7", price=500, quantity=250, maximum=1)

best_buy = store.Store([mac, bose])
mac.price = -100         # Should give error
print(mac)               # Should print `MacBook Air M2, Price: $1450 Quantity:100`
print(mac > bose)        # Should print True
print(mac in best_buy)   # Should print True
print(pixel in best_buy) # Should print False

"""