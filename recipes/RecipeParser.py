import json
import re

from .Recipe import Recipe

class RecipeParser:

    wowhead_type = 'spell'
    parser_type = 'recipe'

#     def parse(content):
        
#         soup = BeautifulSoup(content, 'html.parser')
        
#         # Example parsing logic for Recipe
#         name = soup.find('h1', class_='heading-size-1').text.strip()
#         ingredients = [ingredient.text.strip() for ingredient in soup.find_all('span', class_='ingredient')]
#         return Recipe(
#             recipe_id: int
#             name: str
#             skill: int
#             trainning_cost: int
#             colors: List[int]
#             creates: Dict[int, int] #item_id: amount
#             reagents: Dict[int, int] #item_id: amount
#             season_id: int = None
#         )