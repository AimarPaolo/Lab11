import string
from dataclasses import dataclass

@dataclass
class Product:
    Product_number: int
    Product_line: string
    Product_type: string
    Product: string
    Product_brand: string
    Product_color: string
    Unit_cost: float
    Unit_price: float

    def __hash__(self):
        return hash(self.Product_number)