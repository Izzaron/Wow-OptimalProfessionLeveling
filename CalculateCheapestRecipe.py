from collections import defaultdict
import json
from math import ceil

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
        self.known_professions = [164,186] #164 is blacksmithing, 186 is mining

    def get_cheapest_recipe_for_level(self, level: int):
        candidates = self.get_candidate_recipes(level)
        print('Print best recipes for level',level)
        cheapest = None
        for recipe in candidates:
            price = self.get_recipe_cost(recipe)
            probability = self.get_levelup_probability(recipe.colors,level)
            # print(format_copper_price(price),str(probability*100)+'%',end=' ')
            nr_required = ceil(1/probability)
            price = price * nr_required
            # self.print_recipe(recipe)
            if cheapest == None or price < cheapest[0]:
                cheapest = (price,recipe)
        return cheapest


    def get_levelup_probability(self,colors,level):
        yellow = int(colors[1])
        gray = int(colors[3])
        return max(min((gray-level)/(gray-yellow),1),0)

    def get_candidate_recipes(self, level: int):
        candidates = []
        for recipe in self.recipe_db.get_all_recipes(skill=164,season_id=0,sort_recipes=True):
            if level < int(recipe.colors[0]):
                break
            if level >= int(recipe.colors[3]):
                continue
            candidates.append(recipe)
        return candidates

    def get_recipe_cost(self,recipe):
        reagents = recipe.reagents.items()
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

    def get_all_recipe_reagents(self,recipe):
        reagents = recipe.reagents.items()
        reagent_list = defaultdict(int)
        for reagent_id,amount in reagents:
            item = self.item_db.getItem(reagent_id)
            if item.created_by:
                recipe = self.recipe_db.get_recipe(item.created_by)
                if recipe.skill in self.known_professions:
                    sub_reagents = self.get_all_recipe_reagents(recipe)
                    for sub_reagent_id,sub_amount in sub_reagents.items():
                        reagent_list[sub_reagent_id] += sub_amount*amount
                else:
                    reagent_list[item.item_id] += amount
            else:
                reagent_list[item.item_id] += amount
        return reagent_list

    def print_recipe(self,recipe):
        print(recipe.name,end=' ')
        print(f"\033[38;2;255;128;64m{recipe.colors[0]}\033[0m",end=' ') #ff8040
        print(f"\033[38;2;255;255;0m{recipe.colors[1]}\033[0m",end=' ') #ffff00
        print(f"\033[38;2;64;191;64m{recipe.colors[2]}\033[0m",end=' ') #40bf40
        print(f"\033[38;2;128;128;128m{recipe.colors[3]}\033[0m",end=' ') #808080
        print('')

if __name__ == '__main__':
    
    rv = RecipeValuator()

    # price,cheapest = rv.get_cheapest_recipe_for_level(1)
    # rv.print_recipe(cheapest)
    # for reagent,amount in rv.get_all_recipe_reagents(cheapest).items():
    #     print(amount,rv.item_db.getItem(reagent).name)
    
    # rdb = RecipeDatabase()
    # recipes = rdb.get_all_recipes(skill=164,season_id=0,sort_recipes=True)
    # for recipe in recipes[10:20]:
    #     print(recipe.name + ":",end=' ')
    #     for reagent,amount in rv.get_all_recipe_reagents(recipe).items():
    #         print(amount,rv.item_db.getItem(reagent).name,end=', ')
    #     print('')

    item_id = 3486
    idb = ItemDatabase()
    item = idb.getItem(item_id)
    print(item)