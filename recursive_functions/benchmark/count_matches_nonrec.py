import sys

sys.setrecursionlimit(10000)

def count_matches(lst, target, acc=0):
    _P = []
    _P.append((lst, target, acc, None, 0))
    while len(_P) > 0:
        lst, target, acc, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and (not lst)):
            if _s == 0:
                _r = acc
                _s = -1
        elif _s in [1] or _s == 0:
            if _s == 0:
                _P.append((lst, target, acc, _r1, 1))
                _P.append((lst[1:], target, acc + (1 if lst[0] == target else 0), None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r = _r1
                _s = -1
    return _r
n = 1000
lst = [1, 2, 3] * (n // 3)
target = 2

# --- benchmark ---
def chamada():
    return count_matches(lst, target)
