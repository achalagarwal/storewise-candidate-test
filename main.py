import traceback
from doctest import UnexpectedException
from typing import List

from bullet import Bullet, colors, utils


class PurchaseItem(object):
    def __init__(self, option):
        self.price = option.p
        self.name = str(option)


def get_total_order_amount(order: List[PurchaseItem]):
    total_amount = sum(item.price for item in order)
    return total_amount


def get_service_charge(order: List[PurchaseItem]):
    total_amount = get_total_order_amount(order)
    service_charge = 0.0
    
    # Calculate service charge
    if total_amount > 0:
        service_charge = min(0.2 * total_amount, 0.01 * total_amount * (total_amount // 100))
    
    return service_charge



class Option(object):
    def __init__(self, n=None, pu=None, p=None, d=None):
        self.p = p
        self.n = n
        self.pu = pu
        if d:
            self.n = d.get("name")
            self.p = d.get("price")
        if self.p == None:
            self.p = 0
        if self.n == None:
            raise AttributeError
        self.pu = self.pu if self.pu else "Rs."

    def __str__(self):
        return f"{str(self.n)} {str(self.pu) + ' ' + str(self.p) if self.p else ''}"

    def __len__(self):
        return len(self.__str__())


MCDONALDS_FOOD_OPTIONS = [
    Option(d={"name": "Veg Burger", "price": 115.00}),
    Option(d={"name": "Veg Wrap", "price": 130.00}),
    Option(d={"name": "Veg Happy Meal", "price": 215.00}),
    Option(d={"name": "Chicken Burger", "price": 175.00}),
    Option(d={"name": "Chicken Wrap", "price": 195.00}),
    Option(d={"name": "No, that's all", "price": 0.00}),
]

MCDONALDS_BEVERAGES_OPTIONS = [
    Option(d={"name": "Sprite (M)", "price": 115.00}),
    Option(d={"name": "Sprite (L)", "price": 130.00}),
    Option(d={"name": "Mango Smoothie", "price": 215.00}),
    Option(d={"name": "Chocolate Smoothie", "price": 175.00}),
    Option(d={"name": "Chocolate Smoothie w/ Icecream", "price": 195.00}),
    Option(d={"name": "No, that's all", "price": 0.00}),
]


def get_option_from_result(result, options):
    for option in options:
        if str(option) == result:
            return option

    raise UnexpectedException

def print_order(order):
    print()

    try:
        total_amount = get_total_order_amount(order)
    except Exception as e:
        traceback.print_exc()
        total_amount = "ERROR"

    try:
        service_charge = get_service_charge(order)
    except Exception as e:
        traceback.print_exc()
        service_charge = "ERROR"

    final_amount = total_amount + service_charge if isinstance(total_amount, (int, float)) and isinstance(service_charge, (int, float)) else 'ERROR'

    utils.cprint(
        "Final Order", color=colors.foreground["green"], on=colors.background["yellow"]
    )
    for i, item in enumerate(order):
        utils.cprint(
            f"{i+1}. {item.name}",
            color=colors.foreground["yellow"],
            on=colors.background["green"],
        )

    utils.cprint(
        f"Order Amount: {str(total_amount)}",
        color=colors.foreground["green"],
        on=colors.background["yellow"],
    )
    utils.cprint(
        f"Service Charge: {str(service_charge)}",
        color=colors.foreground["green"],
        on=colors.background["yellow"],
    )
    utils.cprint(
        f"Final Amount: {str(final_amount)}",
        color=colors.foreground["green"],
        on=colors.background["yellow"],
    )


print()
utils.cprint(
    "Welcome to McDonalds on your shell :)",
    color=colors.foreground["blue"],
    on=colors.background["white"],
)
utils.cprint(
    "Here you can place your order        ",
    color=colors.foreground["blue"],
    on=colors.background["white"],
)
utils.cprint(
    "And then we will show you your bill  ",
    color=colors.foreground["blue"],
    on=colors.background["white"],
)
print()
order = []
while True:
    options = list(map(lambda x: str(x), MCDONALDS_FOOD_OPTIONS))
    bullet = Bullet(prompt="Add an item", choices=options, bullet="=> ")
    result = bullet.launch()
    utils.clearConsoleUp(7)
    option = get_option_from_result(result, MCDONALDS_FOOD_OPTIONS)
    if result == str(MCDONALDS_FOOD_OPTIONS[-1]):
        break
    order.append(PurchaseItem(option))
    utils.cprint(
        f"{result} is added to your order", on=colors.background["green"], end="\n"
    )

while True:
    options = list(map(lambda x: str(x), MCDONALDS_BEVERAGES_OPTIONS))
    bullet = Bullet(prompt="Add a beverage", choices=options, bullet="=> ")
    result = bullet.launch()
    utils.clearConsoleUp(7)
    option = get_option_from_result(result, MCDONALDS_BEVERAGES_OPTIONS)
    if result == str(MCDONALDS_BEVERAGES_OPTIONS[-1]):
        break
    order.append(PurchaseItem(option))
    utils.cprint(
        f"{result} is added to your order", on=colors.background["green"], end="\n"
    )

utils.clearConsoleUp(1)
print()

print_order(order)
