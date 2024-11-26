from items.Item import Item
from items.ItemDatabase import ItemDatabase
from recipes.Recipe import Recipe
from recipes.RecipeDatabase import RecipeDatabase
import json

def data_from_recipe_db(data):
    recipe_db = RecipeDatabase()
    for recipe in data:
        new_recipe = Recipe(
            recipe['id'],
            recipe['name'],
            164,
            0,
            recipe['colors'],
            {recipe['creates'][0]: recipe['creates'][1]},
            {k:v for k,v in recipe['reagents']}
        )
        if 'seasonId' in recipe:
            new_recipe.season_id = recipe['seasonId']
        recipe_db.add_recipe(new_recipe)
    recipe_db.save()

def basic_populate():
    idb = ItemDatabase()
    idb.addItem(Item(2589, 'Linen Cloth', 5))
    idb.addItem(Item(2835, 'Rough Stone', 2))
    idb.addItem(Item(2770, 'Copper Ore', 7))
    idb.addItem(Item(2840, 'Copper Bar', 20, 2657))
    idb.addItem(Item(2880, 'Weak Flux', 105))
    idb.addItem(Item(2863, 'Coarse Sharpening Stone', 5))
    idb.save()
    print(idb.count())

    rdb = RecipeDatabase()
    rdb.add_recipe(Recipe(2657,'Smelt Copper',186,0,[0,25,47,70],{2840: 1},{2770: 1}))
    rdb.save()
    print(rdb.count())

def open_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()
    return json.loads(content)

if __name__ == '__main__':
    # file_path = 'recipes/sorted_blacksmithing.json'
    # data = open_json(file_path)
    
    # data_from_recipe_db(data)
    basic_populate()