from dataclasses import dataclass
from typing import Dict, List

@dataclass
class Recipe:
    recipe_id: int
    name: str
    skill: int
    trainning_cost: int
    colors: List[int]
    creates: Dict[int, int] #item_id: amount
    reagents: Dict[int, int] #item_id: amount
    season_id: int = None

    def __post_init__(self):
        self.recipe_id = int(self.recipe_id)
        self.name = str(self.name)
        self.skill = int(self.skill)
        self.trainning_cost = int(self.trainning_cost)
        if not isinstance(self.colors, list) or len(self.colors) != 4:
            raise Exception("Colors must be a list of 4 integers")
        if not isinstance(self.creates, dict):
            raise Exception("Creates must be a dictionary")
        if not isinstance(self.reagents, dict):
            raise Exception("Reagents must be a dictionary")
    
    def __str__(self):
        string = f"{self.name} (s{self.recipe_id}) "
        string += f"\033[38;2;255;128;64m{self.colors[0]}\033[0m " #ff8040
        string += f"\033[38;2;255;255;0m{self.colors[1]}\033[0m " #ffff00
        string += f"\033[38;2;64;191;64m{self.colors[2]}\033[0m " #40bf40
        string += f"\033[38;2;128;128;128m{self.colors[3]}\033[0m " #808080
        return string