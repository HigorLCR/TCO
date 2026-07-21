from typing import Callable

def find_first(lst: list, pred: Callable, idx: int=0):
    while not (idx >= len(lst) or pred((val := lst[idx]))):
        lst, pred, idx = (lst, pred, idx + 1)
    if idx >= len(lst):
        return None
    else:
        return val


n = 10_00
lst = list(range(n))
pred = lambda x: x > 5_000

# --- benchmark ---
def chamada():
    return find_first(lst, pred)
