"""Main program for the text_based adventure game.

This script imports functions from gamefunctions.py and runs
a simple interactive game with user input.
"""

import gamefunctions

name = input("Enter your name: ")

gamefunctions.print_welcome(name, 30)
gamefunctions.print_shop_menu("Sword", 100, "Shield", 75)

monster = gamefunctions.new_random_monster()
print(monster)
