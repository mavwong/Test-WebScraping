from dataclasses import dataclass
from typing import List, Optional
import pydantic

@dataclass
class Product:
    page_no: int
    manufacturer: str
    title: str
    price: str
    description: str


if __name__ == "__main__":
    None