from dataclasses import dataclass

@dataclass
class Item:
    id:         int
    name:       str
    price:      int
    created_by: int = None

    def __post_init__(self):
        self.id = int(self.id)
        self.name = str(self.name)
        self.price = int(self.price)
        if self.created_by:
            self.created_by = int(self.created_by)