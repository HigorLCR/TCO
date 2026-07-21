import sys
from typing import Callable

sys.setrecursionlimit(100_000)


def find_first(lst: list, pred: Callable, idx: int = 0):
    if idx >= len(lst):
        return None
    elif pred(val := lst[idx]):
        return val
    else:
        return find_first(lst, pred, idx + 1)


n = 10_00
lst = list(range(n))
pred = lambda x: x > 5_000

# --- benchmark ---
def chamada():
    return find_first(lst, pred)
