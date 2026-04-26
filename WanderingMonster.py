"""Module containing the WanderingMonster class."""

import random

class WanderingMonster:
    """Stores and controls one wandering monster on the map."""
    def __init__(self, x, y, monster_type, color, hp):
        self.x = x
        self.y = y
        self.monster_type = monster_type
        self.color = color
        self.hp = hp

    def random_spawn(self, occupied, forbidden, grid_w, grid_h):
        """Randomly assigns this monster to a valid location"""
        while True:
            new_x = random.randint(0, grid_w - 1)
            new_y = random.randint(0, grid_h - 1)

            if (new_x, new_y) not in occupied and (new_x, new_y) not in forbidden:
                self.x = new_x
                self.y = new_y
                break

    def from_dict(self, data):
        """Loads this monster's data from a dictionary"""
        self.x = data["x"]
        self.y = data["y"]
        self.monster_type = data["monster_type"]
        self.color = data["color"]
        self.hp = data["hp"]

    def to_dict(self):
        """Converts this monster into JSON-safe dictionary data."""
        return {
            "x": self.x,
            "y": self.y,
            "monster_type": self.monster_type,
            "color": list(self.color),
            "hp": self.hp
        }

    def move(self, occupied, forbidden, grid_w, grid_h):
        """
        Attempts to move the monster in a random direction.
        If the move is invalid, the monster stays put.
        """
        directions = [
            (0, -1), # up
            (0, 1),  # down
            (-1, 0), # left
            (1,0),   # right
        ]

        dx, dy = random.choice(directions)

        new_x = self.x + dx
        new_y = self.y + dy

        if new_x < 0 or new_x >= grid_w:
            return

        if new_y < 0 or new_y >= grid_h:
            return

        if (new_x, new_y) in occupied:
            return

        if (new_x, new_y) in forbidden:
            return

        self.x = new_x
        self.y = new_y

























        
