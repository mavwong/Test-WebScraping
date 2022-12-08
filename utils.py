from typing import List

def flatten_lists(x: List[list]) -> List[dict]:
    return sum(x, [])