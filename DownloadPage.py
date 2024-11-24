import requests

def download(item_type:str, item_id: int):
    url = 'https://www.wowhead.com/classic/' + item_type + '=' + str(item_id)
    filename = item_type + str(item_id) + '.html'
    try:
        response = requests.get(url)
        response.raise_for_status()  # Check if the request was successful
        with open(filename, 'w', encoding='utf-8') as file:
            file.write(response.text)
        print(f"Page downloaded and saved to {filename}")
    except requests.exceptions.RequestException as e:
        print(f"An error occurred: {e}")

# Example usage
item = 2880
download('item',item)