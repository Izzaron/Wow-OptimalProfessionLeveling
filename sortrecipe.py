import json

def sort_recipes_by_learnedat(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        recipes = json.load(file)
    
    # Sort recipes by the 'learnedat' field
    sorted_recipes = sorted(recipes, key=lambda x: x['learnedat'])
    
    with open(output_file, 'w', encoding='utf-8') as file:
        json.dump(sorted_recipes, file, separators=(',', ':'))
    
    print(f"Sorted recipes have been written to {output_file}")

# Example usage
input_file = 'recipes/blacksmithing.json'
output_file = 'recipes/sorted_blacksmithing.json'
sort_recipes_by_learnedat(input_file, output_file)