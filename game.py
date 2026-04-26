"""Main program for the text_based adventure game.

This script imports functions from gamefunctions.py and runs
a simple interactive game with user input.
"""

import gamefunctions
import random
import json
from WanderingMonster import WanderingMonster

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
                       "1) Explore\n"
                       "2) Sleep (Restore HP for 5 gold)\n"
                       "3) Shop \n"
                       "4) Save and Quit\n"
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
    if player_hp <= 0:
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


def save_game(state, filename="save.json"):
    save_state = state.copy()

    save_state["monsters"] = []
    for monster in state["monsters"]:
        save_state["monsters"].append(monster.to_dict())

    save_state["current_monster"] = None
    
    with open(filename, "w") as f:
        json.dump(save_state, f, indent=4)
    print("Game saved!")


def load_game(filename="save.json"):
    try:
        with open(filename, "r") as f:
            state = json.load(f)

        loaded_monsters = []

        for monster_data in state.get("monsters", []):
            monster = WanderingMonster(0, 0, "Goblin", [0, 255, 0], 20)
            monster.from_dict(monster_data)
            loaded_monsters.append(monster)

        state["monsters"] = loaded_monsters
        state["current_monster"] = None

        print("Game loaded!")
        return state
    except FileNotFoundError:
        print("No save file found.")
        return None


def spawn_monster(state):
    map_state = state["map_state"]

    occupied = []
    for monster in state["monsters"]:
        occupied.append((monster.x, monster.y))

    forbidden = [
        (map_state["player_x"], map_state["player_y"]),
        (map_state["town_x"], map_state["town_y"])
    ]

    new_monster = WanderingMonster(0, 0, "Goblin", [0, 255, 0], 20)
    new_monster.random_spawn(occupied, forbidden, 10, 10)

    state["monsters"].append(new_monster)


def move_player(game_state, direction):
    """
    diretion is one of: 'up', 'down', 'left', 'right'
    Updates map_stat.
    Returns:
        "moved"
        "returned_to_town"
        "monster_encounter"
    """
    map_state = game_state["map_state"]
    x = map_state["player_x"]
    y = map_state["player_y"]

    old_x = x
    old_y = y

    if direction == "up" and y > 0:
        y -= 1
    elif direction == "down" and y < 9:
        y += 1
    elif direction == "left" and x > 0:
        x -= 1
    elif direction == "right" and x < 9:
        x += 1

    map_state["player_x"] = x
    map_state["player_y"] = y

    if x == old_x and y == old_y:
        return "moved"

    if (x, y) == (map_state["town_x"], map_state["town_y"]) and (old_x, old_y) != (x, y):
      return "returned_to_town"

    for monster in game_state["monsters"]:
        if (x, y) == (monster.x, monster.y):
            game_state["current_monster"] = monster
            return "monster_encounter"

    return "moved"
            
                                                               
def print_map(state):
    map_state = state["map_state"]

    for y in range(10):
        row = ""
        for x in range (10):
            if x == map_state["player_x"] and y == map_state["player_y"]:
                row += "P"
            elif x == map_state["town_x"] and y == map_state["town_y"]:
                row += "T"
            else:
                monster_here = False

                for monster in state["monsters"]:
                    if x == monster.x and y == monster.y:
                        monster_here = True

                if monster_here:
                    row += "M"
                else:
                    row += "."
        print(row)


def move_all_monsters(state):
    map_state = state["map_state"]

    forbidden = [
        (map_state["player_x"], map_state["player_y"]),
        (map_state["town_x"], map_state["town_y"])
    ]

    for monster in state["monsters"]:
        occupied = []

        for other_monster in state["monsters"]:
            if other_monster != monster:
                occupied.append((other_monster.x, other_monster.y))

        monster.move(occupied, forbidden, 10, 10)


def run_map_interface(state):
    while True:
        print("\nMap:")
        print_map(state)
        print("Move with w/a/s/d")

        move = input("Enter move: ").lower()

        if move == "w":
            result = move_player(state, "up")
        elif move == "s":
            result = move_player(state, "down")
        elif move == "a":
            result = move_player(state, "left")
        elif move == "d":
            result = move_player(state, "right")
        else:
            print("Invalid move.")
            continue
        if result == "returned_to_town":
            print("You returned to town.")
            return "town"
        elif result == "monster_encounter":
            print("A monster appears!")
            return "monster"

        move_all_monsters(state)



# Main Game Loop
def main():
    """
    Runs the main game loop, allowing the player to fight, sleep, or quit.
    """
    print("1) New Game")
    print("2) Load Game")
    start_choice = input("Choose: ")
    if start_choice == "1":
        name = input("Enter your name: ")
        gamefunctions.print_welcome(name, 30)
        state = {
            "player_name": name,
            "player_hp": 30,
            "player_gold": 100,
            "player_inventory": [],
            "map_state": {
                "player_x": 0,
                "player_y": 0,
                "town_x": 0,
                "town_y": 0
            },
            "monsters": [],
            "current_monster": None
        }

        spawn_monster(state)


                
    elif start_choice == "2":
        filename = input("Enter filename to load (or press Enter for default): ")
        if filename == "":
            filename = "save.json"
        state = load_game(filename)
        if state is None:
            print("Starting new game instead...")
            name = input("Enter your name: ")
            gamefunctions.print_welcome(name, 30)
            state = {
                "player_name": name,
                "player_hp": 30,
                "player_gold": 100,
                "player_inventory": [],
                "map_state": {
                "player_x": 0,
                "player_y": 0,
                "town_x": 0,
                "town_y": 0,
             },
            "monsters": [],
            "current_monster": None
        }

        spawn_monster(state)
        
    else:
        print("Invalid choice.")
        return

    playing = ["yes"]
    while playing == ["yes"]:
        print(f"\nYou are in town.")
        print(f"Current HP: {state['player_hp']}, Current Gold: {state['player_gold']}")

        choice = get_menu_choice()

        if choice == "1":
            exploring = True
            while exploring:
                map_result = run_map_interface(state)
                if map_result == "town":
                    exploring = False
                elif map_result == "monster":
                    state = fight_monster(state)
                    if state["player_hp"] <= 0:
                        print("Game Over.")
                        playing = []
                        exploring = False
                    else:
                        defeated_monster = state["current_monster"]

                        if defeated_monster in state["monsters"]:
                            state["monsters"].remove(defeated_monster)

                        state["current_monster"] = None

                        if len(state["monsters"]) == 0:
                            spawn_monster(state)
                            spawn_monster(state)

        elif choice == "2":
            state = sleep(state)

        elif choice == "3":
            state = shop(state)

        elif choice == "4":
            filename = input("Enter filename (or press Enter for default): ")
            if filename == "":
                filename = "save.json"
            save_game(state, filename)
            print("Goodbye!")
            playing = []

        elif choice == "5":
            state = equip_weapon(state)
    

if __name__ == "__main__":
    main()











        
