from typing import Dict
from dataclasses import asdict
import json
from .Recipe import Recipe
import os

class RecipeDatabase:
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), 'recipes.json')
        self.recipes: Dict[int, Recipe] = dict()
        self.load()
        # print(f"Loaded {len(self.recipes)} recipes from {self.file_path}")

    def load(self):
        # Load items from a JSON file
        with open(self.file_path, 'r', encoding='utf-8') as file:
            recipes = json.load(file)
        
        # Convert items to Item objects
        self.recipes = {int(recipe_id): Recipe(**recipe) for recipe_id, recipe in recipes.items()}
    
    def save(self):
        # Convert items to a serializable format
        serializable_recipes = {recipe_id: asdict(recipe) for recipe_id, recipe in self.recipes.items()}
        
        # Save items to a JSON file
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(serializable_recipes, file, separators=(',', ':'))

    def count(self):
        return len(self.recipes)

    def add_recipe(self, recipe):
        if recipe.id in self.recipes:
            print(f"Item {recipe.id} already exists, aborting add operation")
            return
            #raise Exception(f"Item {recipe.id} already exists")
        if not isinstance(recipe.id, int):
            raise Exception("Item ID must be an integer")
        # Add an item to the database
        self.recipes[recipe.id] = recipe

    def get_recipe(self, recipe_id):
        recipe_id = int(recipe_id)
        # Return an item by its ID
        if recipe_id not in self.recipes:
            # Fetch the item from the database
            raise Exception(f"Recipe {recipe_id} not found")
        return self.recipes[recipe_id]
    
    def get_all_recipes(self, skill=None, season_id=None,sort_recipes=False):
        
        recipes = list(self.recipes.values())
        if skill:
            recipes = [recipe for recipe in recipes if recipe.skill == skill]
        if not season_id is None:
            if season_id == 0:
                recipes = [recipe for recipe in recipes if recipe.season_id == None]
            else:
                recipes = [recipe for recipe in recipes if recipe.season_id == season_id]
            
        if sort_recipes:
            recipes = sorted(recipes, key=lambda recipe: recipe.colors[0])
        return recipes