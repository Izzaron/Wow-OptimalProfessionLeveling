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