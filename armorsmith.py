from RecipeValuator import RecipeValuator
from collections import defaultdict

armorsmith_recipes = {
    7223 : 6,
    9968 : 2,
    9945 : 1,
    9961 : 2,
    9952 : 1,
    9959 : 2,
    9950 : 1,
    9980 : 4,
    9979 : 2,
    9972 : 1
}

additional_items = {
    3860 : 40+40+40,
    3575 : 40,
    3864 : 4,
    6037 : 40
}

if __name__ == "__main__":
    rv = RecipeValuator([164,186])

    print('')
    print("Mats needed for Armorsmithing:")

    mats_total = defaultdict(int)

    for recipe_id,amount in armorsmith_recipes.items():
        recipe = rv.recipe_db.get_recipe(recipe_id)
        reagents = rv.get_all_recipe_reagents(recipe)
        for reagent_id,sub_amount in reagents.items():
            item = rv.item_db.get_item(reagent_id)
            mats_total[item.item_id] += sub_amount*amount

    for item_id,amount in additional_items.items():
        item = rv.item_db.get_item(item_id)
        if item.created_by:
            recipe = rv.recipe_db.get_recipe(item.created_by)
            mats = rv.get_all_recipe_reagents(recipe)
            for reagent_id,sub_amount in mats.items():
                mats_total[reagent_id] += sub_amount*amount
        else:
            mats_total[item.item_id] += amount

    for mat in mats_total.items():
        print(f"{mat[1]} {rv.item_db.get_item(mat[0]).name}")

    print('')
    print("Recipes needed for Armorsmithing:")

    # Recipes needed for Armorsmithing:
    for recipe_id,amount in armorsmith_recipes.items():
        recipe = rv.recipe_db.get_recipe(recipe_id)
        print(f"{amount} {recipe}")