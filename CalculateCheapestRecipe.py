import json

from items.ItemDatabase import ItemDatabase
from recipes.RecipeDatabase import RecipeDatabase
from PriceFormatter import format_copper_price

def open_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return json.loads(content)
    
class RecipeValuator:
    def __init__(self):
        self.item_db = ItemDatabase()
        self.recipe_db = RecipeDatabase()
        self.known_professions = [186,164] #186 is mining, 164 is blacksmithing

    def get_cheapest_recipe_for_level(self,data, level: int):
        candidates = self.get_candidate_recipes(data, level)
        print('Print best recipes for level',level)
        for recipe in candidates:
            price = self.get_recipe_cost(recipe)
            probability = self.get_levelup_probability(recipe['colors'],level)
            print(format_copper_price(price),str(probability*100)+'%',end=' ')
            self.print_recipe(recipe)
        
    def get_levelup_probability(self,colors,level):
        yellow = int(colors[1])
        gray = int(colors[3])
        return max(min((gray-level)/(gray-yellow),1),0)

    def get_candidate_recipes(self,data, level: int):
        candidates = []
        for recipe in data:
            if 'seasonId' in recipe:
                continue
            if level < int(recipe['colors'][0]):
                break
            if level >= int(recipe['colors'][3]):
                continue
            candidates.append(recipe)
        return candidates

    def get_recipe_cost(self,recipe):
        reagents = recipe['reagents']
        cost = 0
        for reagent_id,amount in reagents:
            cost += self.get_reagent_cost(reagent_id)*amount
        return cost

    def get_reagent_cost(self,reagent_id):
        item = self.item_db.getItem(reagent_id)
        if item.created_by:
            recipe = self.recipe_db.get_recipe(item.created_by)
            if recipe.skill in self.known_professions:
                total_reagent_cost = 0
                for reagent_id,amount in recipe.reagents.items():
                    total_reagent_cost += self.get_reagent_cost(reagent_id)*amount
                if total_reagent_cost < item.price:
                    return total_reagent_cost
                
        return item.price

    def print_recipe(self,recipe):
        print(recipe['name'],end=' ')
        print(f"\033[38;2;255;128;64m{recipe['colors'][0]}\033[0m",end=' ') #ff8040
        print(f"\033[38;2;255;255;0m{recipe['colors'][1]}\033[0m",end=' ') #ffff00
        print(f"\033[38;2;64;191;64m{recipe['colors'][2]}\033[0m",end=' ') #40bf40
        print(f"\033[38;2;128;128;128m{recipe['colors'][3]}\033[0m",end=' ') #808080
        print('')

if __name__ == '__main__':
    file_path = 'recipes/sorted_blacksmithing.json'
    data = open_json(file_path)

    rv = RecipeValuator()

    rv.get_cheapest_recipe_for_level(data, 19)