import math
import sys

sys.setrecursionlimit(10000)

def sum_nested(data):
    _P = []
    _P.append((data, None, None, None, 0))
    while len(_P) > 0:
        data, _r1, _r2, _r3, _s = _P.pop()
        if _s == 0:
            _r = None
        match data:
            case None | False:
                if _s == 0:
                    _r = 0
                    _s = -1
            case math.inf:
                if _s == 0:
                    _r = 0
                    _s = -1
            case int(n):
                if _s == 0:
                    _r = n
                    _s = -1
            case []:
                if _s == 0:
                    _r = 0
                    _s = -1
            case [head, *tail]:
                if _s == 0:
                    _P.append((data, _r1, _r2, _r3, 1))
                    _P.append((head, None, None, None, 0))
                    _s = -1
                elif _s == 1:
                    _r1 = _r
                    _s = 0
                if _s == 0:
                    _P.append((data, _r1, _r2, _r3, 2))
                    _P.append((tail, None, None, None, 0))
                    _s = -1
                elif _s == 2:
                    _r2 = _r
                    _s = 0
                if _s == 0:
                    _r = _r1 + _r2
                    _s = -1
            case {'value': v}:
                if _s == 0:
                    _P.append((data, _r1, _r2, _r3, 3))
                    _P.append((v, None, None, None, 0))
                    _s = -1
                elif _s == 3:
                    _r3 = _r
                    _s = 0
                if _s == 0:
                    _r = _r3
                    _s = -1
            case _ as unknown:
                if _s == 0:
                    _r = 0
                    _s = -1
    return _r
nested = [1, [2, [3, 4]], [5, 6], {'value': 7}, None, False]

# --- benchmark ---
def chamada():
    return sum_nested(nested)
