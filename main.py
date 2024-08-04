import traceback
from typing import List

import questionary

class PurchaseItem(object):
    def __init__(self, option):
        self.price = option.p
        self.name = str(option)

def get_total_order_amount(order):
    return sum(item.price for item in order)

def get_service_charge(order):
    order_amount = get_total_order_amount(order)
    service_charge_percentage = min((order_amount // 100) * 0.01, 0.20)
    return order_amount * service_charge_percentage

class Option(object):
    def __init__(self, n=None, pu=None, p=None, d=None):
        self.p = p
        self.n = n
        self.pu = pu
        if d:
            self.n = d.get("name")
            self.p = d.get("price")
        if self.p is None:
            self.p = 0
        if self.n is None:
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
    raise ValueError("Option not found")

def print_order(order):
    print()
    try:
        total_amount = get_total_order_amount(order)
    except Exception:
        traceback.print_exc()
        total_amount = "ERROR"

    service_charge = "ERROR"
    if total_amount != "ERROR":
        try:
            service_charge = get_service_charge(order)
        except Exception:
            traceback.print_exc()
            service_charge = "ERROR"

    print("\nFinal Order")
    for i, item in enumerate(order):
        print(f"{i+1}. {item.name}")

    print(f"\nOrder Amount: {str(total_amount)}")
    print(f"Service Charge: {str(service_charge)}")
    print(f"Final Amount: {str(total_amount + service_charge) if isinstance(total_amount, (int, float)) and isinstance(service_charge, (int, float)) else 'ERROR'}")

def main():
    print("\nWelcome to McDonalds on your shell :)")
    print("Here you can place your order")
    print("And then we will show you your bill\n")

    order = []

    while True:
        result = questionary.select(
            "Add an item",
            choices=[str(option) for option in MCDONALDS_FOOD_OPTIONS]
        ).ask()

        option = get_option_from_result(result, MCDONALDS_FOOD_OPTIONS)
        if result == str(MCDONALDS_FOOD_OPTIONS[-1]):
            break
        order.append(PurchaseItem(option))
        print(f"{result} is added to your order")

    while True:
        result = questionary.select(
            "Add a beverage",
            choices=[str(option) for option in MCDONALDS_BEVERAGES_OPTIONS]
        ).ask()

        option = get_option_from_result(result, MCDONALDS_BEVERAGES_OPTIONS)
        if result == str(MCDONALDS_BEVERAGES_OPTIONS[-1]):
            break
        order.append(PurchaseItem(option))
        print(f"{result} is added to your order")

    print_order(order)

if __name__ == "__main__":
    main()
