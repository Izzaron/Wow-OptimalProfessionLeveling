from items.Item import Item
from items.ItemDatabase import ItemDatabase
from recipes.Recipe import Recipe
from recipes.RecipeDatabase import RecipeDatabase

idb = ItemDatabase()
idb.addItem(Item(2589, 'Linen Cloth', 5))
idb.addItem(Item(2835, 'Rough Stone', 2))
idb.addItem(Item(2770, 'Copper Ore', 7))
idb.addItem(Item(2840, 'Copper Bar', 20, 2657))
idb.addItem(Item(2880, 'Weak Flux', 105))
idb.save()
print(idb.count())

rdb = RecipeDatabase()
rdb.add_recipe(Recipe(2657,'Smelt Copper',186,0,[0,25,47,70],{2840: 1},{2770: 1}))
rdb.save()
print(rdb.count())