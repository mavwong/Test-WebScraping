from dataclasses import dataclass
from typing import List, Optional
import pydantic

@dataclass
class Product:
    manufacturer: str
    title: str
    price: str
    description: str
    #page_no: Optional[int]
    

    
if __name__ == "__main__":
    None