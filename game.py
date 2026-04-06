"""Main program for the text_based adventure game.

This script imports functions from gamefunctions.py and runs
a simple interactive game with user input.
"""

import gamefunctions
import random

def get_menu_choice():
    """
    Prompts the user for a menu choice in town.
    Returns:
        str: The validated manu choice ("1", "2", or "3").
    """
    choice = ""
    valid_choices = ["1", "2", "3", "4", "5"]

    while choice not in valid_choices:
        choice = input("\nWhat would you like to do?\n"
                       "1) Leave town (Fight Monster)\n"
                       "2) Sleep (Restore HP for 5 gold)\n"
                       "3) Shop \n"
                       "4) Quit\n"
                       "5) Equip Weapon\n"
                       "Enter choice: ")
        if choice in valid_choices:
            return choice
        else:
            print("invalid choice. Try again.")


def get_fight_action():
    """
    Prompts the user for a fight action during combat.
    Returns:
        str: The validated fight action ("1" for attack, "2" for run).
    """
    choice = ""
    valid_choices = ["1", "2"]

    while choice not in valid_choices:
        choice = input("\n1) Attack\n2) Run\nEnterChoice: ")

        if choice in valid_choices:
            return choice
        else:
            print("Invalid choice. Try again.")


def fight_monster(state):
    """
    Handles the fight sequence with a randomly generated monster, with a chance to hit or miss
    Parameters:
        player_hp (int): the player's current HP.
        player_gold (int): the player's current gold.
    Returns:
        tuple: Updated (player_hp, player_gold) after the fight.
    """
    monster = gamefunctions.new_random_monster()

    player_hp = state["player_hp"]
    player_gold = state["player_gold"]

    print(f"\nYou encountered {monster['name']}!")
    print(monster["description"])

    # check for instant-kill item
    for item in state["player_inventory"][:]:
        if item["type"] == "consumable":
            print("You used a monster potion and instantly defeated the monster!")
            state["player_inventory"].remove(item)
            state["player_gold"] += monster["money"]
            return state

    fight_active = True
    while fight_active and player_hp > 0 and monster["health"] > 0:
        print(f"\nYour HP: {player_hp} | Monster HP: {monster['health']}")
        action = get_fight_action()

        if action == "1":
            # 70% change to hit
            if random.randint(1, 100) <= 70:
                player_damage = 10

                for item in state["player_inventory"]:
                    if item.get("equipped") and item["type"] == "weapon":
                        player_damage += 5
                        item["currentDurability"] -= 1

                        if item ["currentDurability"] <= 0:
                            print("Your sword broke!")
                            state["player_inventory"].remove(item)
                        break                      
                
                monster["health"] -= player_damage
                print(f"HELL YEAH! You dealt {player_damage} damage.")
            else:
                print("Shit. You missed.")

            if monster["health"] > 0:
                #80% chance monster hits
                if random.randint(1, 100) <= 80:
                    player_hp -= monster ["power"]
                    print(f"Dag nabbit! {monster['name']} hit you for {monster['power']} damage!")
                else:
                    print(f"{monster['name']} missed you!")
            
        elif action == "2":
            print("You ran away")
            fight_active = False 

    # After fight
    if state["player_hp"] <= 0:
        print("You were defeated...")
    elif monster["health"] <= 0:
        print("You defeated the monster!")
        print(f"you gained {monster['money']} gold!")
        player_gold += monster["money"]

    state["player_hp"] = player_hp
    state["player_gold"] = player_gold
    return state


def sleep(state):
    """
    Handles the player sleeping to restore HP.
    Parameters:
        player_hp (int): The player's current HP.
        player_gold (int): The player's current gold.
    Returns:
        Updated (player_hp, player_gold) after sleeping.
    """
    if state["player_gold"] >= 5:
        state["player_gold"] -= 5
        state["player_hp"] += 10
        print("You feel rested. (+10 HP)")
    else:
        print("Not enough gold!")
    return state

def create_sword():
    """This function creates a sword, establishes its qualities, and keeps track
    of its equipped status"""
    return{
        "name": "sword",
        "type": "weapon",
        "maxDurability": 10,
        "currentDurability": 10,
        "equipped": False
}

def create_potion():
    """This function creates a potion, establishes its qualities (i.e., name,
    type, and effect)"""
    return{
        "name": "monster potion",
        "type": "consumable",
        "effect": "kill_monster"
}

def shop(state):
    """
    This function emulates a shop in the game and offers items like the sword
    or monster potion (called by their respective functions) for a specified price
    """
    print("\nWelcome to the shop!")
    print("1) Sword (20 gold)")
    print("2) Monster Potion (15 gold)")
    print("3) Leave shop")

    choice = input("Choose: ")

    if choice == "1":
        if state["player_gold"] >= 20:
            state["player_gold"] -= 20
            state["player_inventory"].append(create_sword())
            print("You bought a sword!")
        else:
            print("Not enough gold!")
    elif choice == "2":
        if state["player_gold"] >= 15:
            state["player_gold"] -= 15
            state["player_inventory"].append(create_potion())
            print("You bought a potion!")
        else:
            print("Not enough gold!")
    return state 

def equip_weapon(state):
    weapons = [item for item in state["player_inventory"] if item["type"] == "weapon"]
    if not weapons:
        print("No weapons to equip.")
        return state

    print("\nChoose weapon to equip:")
    for i, weapon in enumerate(weapons):
        print(f"{i+1}) {weapon['name']}")

    choice = int(input("Choice: ")) - 1

    for weapon in weapons:
        weapon["equipped"] = False

    weapons[choice]["equipped"] = True
    print(f"You equipped {weapons[choice]['name']}!")

    return state

# Main Game Loop
def main():
    """
    Runs the main game loop, allowing the player to fight, sleep, or quit.
    """
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name, 30)

    state = {
        "player_name": name,
        "player_hp": 30,
        "player_gold": 100,
        "player_inventory": [],
}
             

    playing = ["yes"]
    while playing == ["yes"]:
        print(f"\nYou are in town.")
        print(f"Current HP: {state['player_hp']}, Current Gold: {state['player_gold']}")

        choice = get_menu_choice()

        if choice == "1":
            state = fight_monster(state)
            if state["player_hp"] <= 0:
                print("Game Over.")
                playing = []

        elif choice == "2":
            state = sleep(state)

        elif choice == "3":
            state = shop(state)

        elif choice == "4":
            print("Goodbye!")
            playing = []

        elif choice == "5":
            state = equip_weapon(state)
    

if __name__ == "__main__":
    main()











        
