from typing import List
from pathlib import Path

def flatten_lists(x: List[list]) -> List[dict]:
    return sum(x, [])

def print_section(input:str = "Section Header") -> None:
    print("-"*50)
    print(f"{input}... ")
    print("-"*50)
    
def validate_dir(path:Path, raise_error:bool=False)->None:
    """ Validate if the folder path exists. """
    if isinstance(path, str):
        path = Path(path)
    
    # Create the folder or raise error
    if not Path.exists(path):
        if raise_error:
            raise FileNotFoundError(f"Directory folder not found.")
        else:
            Path.mkdir(path)

if __name__ == "__main__":
    None