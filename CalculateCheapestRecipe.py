from collections import defaultdict
import json
from math import ceil

from items.ItemDatabase import ItemDatabase
from recipes.RecipeDatabase import RecipeDatabase
from PriceFormatter import format_copper_price
    
class RecipeValuator:
    def __init__(self, known_professions=None):
        self.item_db = ItemDatabase()
        self.recipe_db = RecipeDatabase()

        #164 is blacksmithing
        #165 is leatherworking
        #171 is alchemy
        #186 is mining
        #197 is tailoring
        #202 is engineering
        #333 is enchanting
        self.known_professions = known_professions

    def get_cheapest_recipe_for_level(self, level: int, print_candidates=False):
        candidates = self.get_candidate_recipes(level)
        cheapest = None
        for recipe in candidates:
            price = self.get_recipe_cost(recipe)
            if print_candidates:
                print('Price for',recipe.name,'is',format_copper_price(price))
            probability = RecipeValuator.get_levelup_probability(recipe.colors,level)
            nr_required = ceil(1/probability)
            price = price * nr_required
            if cheapest == None or price < cheapest[0]:
                cheapest = (price,recipe,nr_required)
        return (cheapest[2],cheapest[1])

    @staticmethod
    def get_levelup_probability(colors,level):
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
        item = self.item_db.get_item(reagent_id)
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
            item = self.item_db.get_item(reagent_id)
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

if __name__ == '__main__':

    rv = RecipeValuator([164,186])

    mats_total = defaultdict(int)
    for lvl in range(30,65):
        times,recipe = rv.get_cheapest_recipe_for_level(lvl)
        mats_total[recipe.recipe_id] += times
        # print(f'Best recipe for level {lvl}: {times} x {recipe.name}')
        # print(recipe)
        # for reagent,amount in rv.get_all_recipe_reagents(recipe).items():
        #     print(times*amount,'x',rv.item_db.get_tem(reagent))
    
    for recipe_id,times in mats_total.items():
        recipe = rv.recipe_db.get_recipe(recipe_id)
        print(times,'x',recipe)
        for reagent,amount in rv.get_all_recipe_reagents(recipe).items():
            print(times*amount,'x',rv.item_db.get_item(reagent))
        print()