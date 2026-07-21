import sys
from typing import Callable

sys.setrecursionlimit(100000)

def find_first(lst: list, pred: Callable, idx: int=0):
    _P = []
    _P.append((lst, pred, idx, None, None, 0))
    while len(_P) > 0:
        lst, pred, idx, val, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and idx >= len(lst)):
            if _s == 0:
                _r = None
                _s = -1
        elif _s in [1] or _s == 0:
            if _s in [] or (_s == 0 and pred((val := lst[idx]))):
                if _s == 0:
                    _r = val
                    _s = -1
            elif _s in [1] or _s == 0:
                if _s == 0:
                    _P.append((lst, pred, idx, val, _r1, 1))
                    _P.append((lst, pred, idx + 1, None, None, 0))
                    _s = -1
                elif _s == 1:
                    _r1 = _r
                    _s = 0
                if _s == 0:
                    _r = _r1
                    _s = -1
    return _r
n = 1000
lst = list(range(n))
pred = lambda x: x > 5000

# --- benchmark ---
def chamada():
    return find_first(lst, pred)
