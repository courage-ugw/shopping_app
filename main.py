import products
import store
import promotions

MENU = """
    Store Menu
    ----------
1. List all products in store
2. Show total amount in store
3. Make an order
4. Quit
please choose a number: 
"""

USER_CHOICE_DICT = {
    1: 'list_all_products',
    2: 'show_total_amount',
    3: 'make_order'
}

QUIT_STORE = 4
ONE = 1


def get_user_choice() -> int:
    """
    Displays Store Menu and Prompts user to choose from the menu.
    validates user's choice and returns user choice
    :return: user_choice (int)
    """
    user_choice = input(MENU)
    choice = is_valid(user_choice, validate_order=False)
    while not choice:
        user_choice = input(MENU)
        choice = is_valid(user_choice)
    return int(user_choice)


def is_valid(user_choice, validate_order=True) -> bool:
    """
    :param user_choice: Gets user_choice and validates user choice. Returns True or False
    :param validate_order: if the validate_order is True the
    function validates user choice from the make_order() function
    :return: True or False (Bool)
    """
    if validate_order:
        if (not user_choice.isdigit()) or (user_choice == 0):
            print(f"Error adding product. Try again!\n")
            return False

    elif not user_choice.isdigit():
        print(f"Error with your choice '{user_choice}'. Try again!")
        return False
    elif int(user_choice) not in [1, 2, 3, 4]:
        print(f"Error with your choice '{user_choice}'. Try again!")
        return False
    return True


def show_total_price(store_obj: object, product: object, product_quantity: str):
    """
    Displays total price (or total price and total item) to the user
    :param store_obj: store object
    :param product: product object (the product the user wants to order)
    :param product_quantity: The amount of item the user wants to order
    :return:
    """
    try:
        total_price, total_item_received = store_obj.order([(product, int(product_quantity))])
        print("Product added to list.")
    except ValueError:
        print()
        pass
    else:
        # checks if buy 2, get 1 free promotion is applied to product
        if total_item_received != 0:
            print(f"The total price of the order is ${total_price} and "
                  f"total is {total_item_received}\n")
        else:
            print(f"The total price of the order is ${total_price}\n")


def start(store_obj: object):
    """
    Gets the Store Object as parameter and Calls the get_user_choice function.
    Calls other functions that executes user's choice,
    """
    user_choice = get_user_choice()
    while user_choice != QUIT_STORE:
        dispatcher = eval(USER_CHOICE_DICT[user_choice])
        dispatcher(store_obj)
        user_choice = get_user_choice()
    print("Thanks for shopping! Bye!")


def list_all_products(store_obj: object) -> list[object]:
    """
    Gets the Object parameter, gets all the products in the store. Prints the list of
    available products to the screen. Returns a list of product objects
    :param store_obj (store object)
    :return: list[product object, ... ]
    """
    all_products = store_obj.get_all_products()
    print("-------------------------------")
    for index, product in enumerate(all_products):
        print(f"{index + ONE}. {product.show()}")
    print("-------------------------------")
    return all_products


def show_total_amount(store_obj: object):
    """
    Gets the Store Object as parameter. Uses the object to fetch the total
    quantity of products in the store and Displays it to the screen
    :param store_obj:
    """
    print("-------------------------------")
    print(f" Total of {store_obj.get_total_quantity()} items in store")
    print("-------------------------------")


def make_order(store_obj: object):
    """
    Gets the store object. Prompts user to make an order by entering a product number
    from the list of products and the quantity of product. If order is successful it
    prints "product added to the list" on the screen. Else it prints an error message
    and prompts user to try again.
    :param store_obj:
    """
    product_number, product_quantity = 0, 0
    all_products = list_all_products(store_obj)
    print('When you finish your order, enter empty text. ')

    while (product_number != '') and (product_quantity != ''):
        product_number = input('Which product # do you want? ')
        product_quantity = input('What amount do you want? ')

        # check for empty text
        if (product_number == '') and (product_quantity == ''):
            continue

        # Validate user choice for both prompts: product number and product quantity
        if is_valid(product_number, validate_order=True) \
                and is_valid(product_quantity, validate_order=True):

            # checks if prdt number is not more than total number of products in store
            if int(product_number) <= len(all_products):

                # checks if prdt qtty is less than the total qtty in store
                product = all_products[int(product_number) - ONE]
                if int(product_quantity) <= product.get_quantity():
                    show_total_price(store_obj, product, product_quantity)

                # checks if the product is non-stocked-product which has unlimited qtty
                elif product.is_non_stocked_product():
                    show_total_price(store_obj, product, product_quantity)

                else:
                    print(f'Error: The amount \'{product_quantity}\' is more than the '
                          'quantity available in the store.\n')
            else:
                print(f"Error adding product. Try again!\n")


def main():
    """ Sets up intial stock of delivery (list of products). Initializes the store
    object and calls the start function. Prints error message to the screen if any"""
    try:
        # setup initial stock of inventory
        product_list = [products.Product("MacBook Air M2", price=1450, quantity=100),
                        products.Product("Bose QuietComfort Earbuds", price=250,
                                         quantity=500),
                        products.Product("Google Pixel 7", price=500, quantity=250),
                        products.NonStockedProduct("Windows License", price=125),
                        products.LimitedProduct("Shipping", price=10, quantity=250,
                                                maximum=1)
                        ]

        # Create promotion catalog
        second_half_price = promotions.SecondHalfPrice("Second Half price!")
        third_one_free = promotions.ThirdOneFree("Third One Free!")
        thirty_percent = promotions.PercentDiscount("30% off!", percent=30)

        # Add promotions to products
        product_list[0].set_promotion(second_half_price)
        product_list[1].set_promotion(third_one_free)
        product_list[3].set_promotion(thirty_percent)

        best_buy = store.Store(product_list)
        start(best_buy)
    except NameError as e:
        print(e)
    except ValueError as e:
        print(e)
    except TypeError as e:
        print(e)


if __name__ == "__main__":
    main()
