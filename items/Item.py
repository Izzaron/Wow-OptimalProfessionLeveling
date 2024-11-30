from dataclasses import dataclass

@dataclass
class Item:
    item_id:    int
    name:       str
    price:      int
    created_by: int = None

    def __post_init__(self):
        self.item_id = int(self.item_id)
        self.name = str(self.name)
        self.price = int(self.price)
        if self.created_by:
            self.created_by = int(self.created_by)
    
    def __str__(self) -> str:
        return f"{self.name} (i{self.item_id}) \033[38;2;255;255;255m{self.price}\033[0m"