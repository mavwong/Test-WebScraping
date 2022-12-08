from typing import List

def flatten_lists(x: List[list]) -> List[dict]:
    return sum(x, [])

def print_section(input:str = "Section Header") -> None:
    print("-"*50)
    print(f"{input}... ")
    print("-"*50)

if __name__ == "__main__":
    None