import json
import re

from .Recipe import Recipe

class RecipeParser:

    wowhead_type = 'spell'
    parser_type = 'recipe'

    def parse(content):
        
        pattern = re.compile(rf'\$\.extend\(g_spells\[(\d+)\],(.*?)\);', re.DOTALL)
        match = pattern.search(content)
        if not match:
            raise ValueError(f"Could not find item data in {content}")
        
        recipe_id = match.group(1)

        recipe_data = str(match.group(2))
        recipe_data = recipe_data.replace('difficulties','"difficulties"')
        
        js = json.loads(recipe_data)

        if len(js['skill']) != 1:
            raise ValueError(f"Expected exactly one skill, got {js['skill']} for recipe {recipe_id}")
        
        if len(js['colors']) != 4:
            raise ValueError(f"Expected exactly four colors, got {js['colors']} for recipe {recipe_id}")
        
        if len(js['creates']) != 3:
            raise ValueError(f"Expected exactly three items in creates, got {js['creates']} for recipe {recipe_id}")

        return Recipe(
            recipe_id=recipe_id,
            name=js['name'],
            skill=js['skill'][0],
            trainning_cost=0,
            colors=js['colors'],
            creates={js['creates'][0]:js['creates'][1]},
            reagents={k:v for k,v in js['reagents']},
            season_id= js['season_id'] if 'season_id' in js else 0
            )