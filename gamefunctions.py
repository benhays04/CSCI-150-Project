
import random


def purchase_item(itemPrice, startingMoney, quantityToPurchase=1):
    """
    Calculates how many items can be purchased given a starting amount of money
    and the price of a single item, and returns the remaining money.
    Parameters:
    itemPrice (float): price of a single item
    startingMoney (float): amount of money available to spend.
    quantityToPurchase (int, optional): desired number of items to purchase
    Returns:
    tuple: a tuple containing:
        - quantity_purchased (int): the numbers of items purchased
        - remaining_money (float): the amount of money left over after
    """
    max_affordable = startingMoney // itemPrice

    quantity_purchased = min(quantityToPurchase, max_affordable)

    remaining_money = startingMoney - (quantity_purchased * itemPrice)

    return quantity_purchased, remaining_money

def new_random_monster():
    """
    Creates and returns a random monster as a dictionary with name, description,
    health, power, and money. Monster type (Goblin, Sea Bear, Robot Tiger) is
    chosen randomly, and its stats are set within specific ranger.
    """
    monster_type = random.choice(["Goblin", "Sea Bear", "Robot Tiger"])

    if monster_type == "Goblin":
        health = random.randint(20, 40)
        power = random.randint(5, 10)
        money = random.randint(10, 50)
        return {
            "name": "A goblin",
            "description": "A nefarious goblin sniffs you in search of spare coins.", 
            "health": health,
            "power": power,
            "money": money
        }

    elif monster_type == "Sea Bear":
        health = random.randint(40, 60)
        power = random.randint(20, 35)
        money = random.randint(15, 30)
        return{
            "name": "Sea Bear",
            "description": "A bulky Sea Bear who has adapted to breathe out of water lumbers towards you.",
            "health": health,
            "power": power,
            "money": money
        }

    elif monster_type == "Robot Tiger":
        health = random.randint(25, 45)
        power = random.randint(15, 30)
        money = random.randint(20, 40)
        return {
            "name": "Robot Tiger",
            "description": "A Robot Tiger, forged from the dark ideas of a mad scientist, pounces into view.",
            "health": health,
            "power": power,
            "money": money
        }

#Demonstrate Code!!!

#First Test purchase_item()

print("Purchase Test 1 (normal purchase):")
num, money = purchase_item(123, 1000, 3)
print(num)
print(money)

print("Purchase Test 2 (cannot afford all of it):")
num, money = purchase_item(123, 201, 3)
print(num)
print(money)

print("Purchase Test 3 (default quantityToPurchase):")
num, money = purchase_item(341, 2112)
print(num)
print(money)

#Second Test new_random_monster()

print("Monster Test 1")
monster1 = new_random_monster()
print(monster1["description"])

print("Monster Test 2")
monster2 = new_random_monster()
print(monster2)

print("Monster 3:")
monster3 = new_random_monster()
print(monster3)


#03/01/2026

def print_welcome(name, width):
    """
    Prints a welcome message for the given 'name', centered within a specified width
    Parameters:
    name (str): The name to include in the welcome.
    width (int): The total width of the field to center the text in.
    Returns: None
    """
    message = f"Hello, {name}!"
    print(message.center(width))

def print_shop_menu(item1Name, item1Price, item2Name, item2Price):
    """
    Prints a menu sign for two items with their prices, with a surrounding border.
    Parameters:
    item1Name (str): Name of the first item. 
    item1Price (float): Price of the first item.
    item2Name (str): Name of the second item.
    item2Price (float): Price of the second item.
    Returns: None
    """
    top_border = "/" + "-"*22 + "\\"
    bottom_border = "\\" + "-"*22 + "/"

    line1 = f"| {item1Name:<12}${item1Price:>7.2f} |"
    line2 = f"| {item2Name:<12}${item2Price:>7.2f} |"

    print(top_border)
    print(line1)
    print(line2)
    print(bottom_border)

#Demonstrate Code!!!

#print_welcome tests:
print_welcome("Ben", 30)
print_welcome("Danny", 25)
print_welcome("Millie", 25)

#print_shop_menu tests:
print_shop_menu("Mushrooms", 200, "Herbal Tea", 50)
print_shop_menu("Stein", 400, "Horse", 420)
print_shop_menu("Backpack", 160, "Rifle", 189)

























    
    
