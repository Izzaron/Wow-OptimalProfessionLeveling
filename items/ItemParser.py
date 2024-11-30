import json
import re

from .Item import Item

class ItemParser:

    wowhead_type = 'item'
    parser_type = 'item'

    def parse(content) -> Item:

        pattern = re.compile(rf'\$\.extend\(g_items\[(\d+)\],(.*?)\);', re.DOTALL)
        match = pattern.search(content)
        if not match:
            raise ValueError(f"Could not find item data in {content}")
        
        item_id = match.group(1)
        item_data = match.group(2)
        js = json.loads(item_data)

        #search for name: WH.TERMS.createdby,
        created_by = None
        pattern = re.compile(r'WH\.TERMS\.createdby.*?"id":(\d+),.*?\}\)\;', re.DOTALL)
        match = pattern.search(content)
        if match:
            created_by = int(match.group(1))

        if 'jsonequip' in js and 'sellprice' in js['jsonequip']:
            sell_price = js['jsonequip']['sellprice']
        else:
            sell_price = 0

        return Item(item_id, js['name'], sell_price, created_by)
