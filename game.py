"""Main program for the text_based adventure game.

This script imports functions from gamefunctions.py and runs
a simple interactive game with user input.
"""

import gamefunctions


def get_menu_choice():
    """
    Prompts the user for a menu choice in town.
    Returns:
        str: The validated manu choice ("1", "2", or "3").
    """
    choice = ""
    valid_choices = ["1", "2", "3"]

    while choice not in valid_choices:
        choice = input("\nWhat would you like to do?\n"
                       "1) Leave town (Fight Monster)\n"
                       "2) Sleep (Restore HP for 5 gold)\n"
                       "3) Quit\n"
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


def fight_monster(player_hp, player_gold):
    """
    Handles the fight sequence with a randomly generated monster, with a chance to hit or miss
    Parameters:
        player_hp (int): the player's current HP.
        player_gold (int): the player's current gold.
    Returns:
        tuple: Updated (player_hp, player_gold) after the fight.
    """
    monster = gamefunctions.new_random_monster()
    monster_hp = monster["health"]

    print(f"\nYou encountered {monster['name']}!")
    print(monster["description"])

    fight_active = True
    while fight_active and player_hp > 0 and monster_hp > 0:
        print(f"\nYour HP: {player_hp} | Monster HP: {monster_hp}")
        action = get_fight_action()

        if action == "1":
            # 70% change to hit
            if random.randint(1, 100) <= 70:
                player_damage = 10
                monster["health"] -= player_damage
                print("HELL YEAH! You dealt 10 damage.")
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
    elif monster_hp <= 0:
        print("You defeated the monster!")
        print(f"you gained {monster['money']} gold!")
        player_gold += monster["money"]

    return player_hp, player_gold


def sleep(player_hp, player_gold):
    """
    Handles the player sleeping to restore HP.
    Parameters:
        player_hp (int): The player's current HP.
        player_gold (int): The player's current gold.
    Returns:
        Updated (player_hp, player_gold) after sleeping.
    """
    if player_gold >= 5:
        player_gold -= 5
        player_hp += 10
        print("You feel rested. (+10 HP)")
    else:
        print("Not enough gold!")

    return player_hp, player_gold

# Main Game Loop
def main():
    """
    Runs the main game loop, allowing the player to fight, sleep, or quit.
    """
    name = input("Enter your name: ")
    gamefunctions.print_welcome(name, 30)

    player_hp = 30
    player_gold = 10

    playing = ["yes"]
    while playing in [["yes"]]:
        print(f"\nYou are in town.")
        print(f"Current HP: {player_hp}, Current Gold: {player_gold}")

        choice = get_menu_choice()

        if choice == "1":
            player_hp, player_gold = fight_monster(player_hp, player_gold)
            if player_hp <= 0:
                print("Game Over.")
                playing = []

        elif choice == "2":
            player_hp, player_gold = sleep(player_hp, player_gold)

        elif choice == "3":
            print("Goodbye!")
            playing = []


if __name__ == "__main__":
    main()











        
