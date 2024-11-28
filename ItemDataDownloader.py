import os
import requests

class ItemDataDownloader:
    @staticmethod
    def download(item_type: str, item_id: int, file_path: str):
        url = f'https://www.wowhead.com/classic/{item_type}={item_id}'
        try:
            response = requests.get(url)
            response.raise_for_status()  # Check if the request was successful
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write(response.text)
            print(f"Page downloaded and saved to {file_path}")
        except requests.exceptions.RequestException as e:
            print(f"An error occurred: {e}")

    @staticmethod
    def parse_html_file(file_path: str, parser):
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
        
        return parser.parse(content)
    
    @staticmethod
    def load_item(item_id: int, parser):

        file_path = f'{parser.parser_type}s/html/{parser.wowhead_type}{item_id}.html'
        
        if os.path.exists(file_path):
            print(f"Using cached data for {parser.parser_type}={item_id} from {file_path}")
        else:
            print(f"{file_path} not found. Downloading {parser.parser_type} data for {item_id}")
            ItemDataDownloader.download(parser.wowhead_type, item_id, file_path)
        
        return ItemDataDownloader.parse_html_file(file_path, parser)
          


# # Example usage

# item_id = 10421 #3470
# item = ItemDataDownloader.load_item(item_id, ItemParser)
# print(item)

# # recipe_id = 2881
# # recipe = ItemDataDownloader.load_item(recipe_id, RecipeParser)
# # print(recipe)