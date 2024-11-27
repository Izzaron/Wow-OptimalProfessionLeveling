from typing import Dict
from dataclasses import asdict
import json
from .Item import Item
import os

class ItemDatabase:
    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), 'items.json')
        self.items: Dict[int, Item] = dict()
        self.load()
        # print(f"Loaded {len(self.items)} items from {self.file_path}")
    
    def load(self):
        # Load items from a JSON file
        with open(self.file_path, 'r', encoding='utf-8') as file:
            items = json.load(file)
        
        # Convert items to Item objects
        self.items = {int(item_id): Item(**item) for item_id, item in items.items()}

    def save(self):
        # Convert items to a serializable format
        serializable_items = {item_id: asdict(item) for item_id, item in self.items.items()}
        
        # Save items to a JSON file
        with open(self.file_path, 'w', encoding='utf-8') as file:
            json.dump(serializable_items, file, separators=(',', ':'))

    def count(self):
        return len(self.items)

    def getItem(self, item_id) -> Item:
        item_id = int(item_id)
        # Return an item by its ID
        if item_id not in self.items:
            # Fetch the item from the database
            raise Exception(f"Item {item_id} not found")
        return self.items[item_id]
    
    def addItem(self, item: Item, reagents=None):
        if item.item_id in self.items:
            return
            #raise Exception(f"Item {item.id} already exists")
        if not isinstance(item.item_id, int):
            raise Exception("Item ID must be an integer")
        # Add an item to the database
        self.items[item.item_id] = item
        if reagents and isinstance(reagents, dict):
            for reagent_id, amount in reagents.items():
                item.reagents[reagent_id] = amount