import sys
sys.setrecursionlimit(100000)

def factorial(n):
    _P = []
    _P.append((n, None, 0))
    while len(_P) > 0:
        n, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n == 0):
            if _s == 0:
                _r = 1
                _s = -1
        elif _s in [1] or _s == 0:
            if _s in [] or (_s == 0 and n == 1):
                if _s == 0:
                    _r = 1
                    _s = -1
            elif _s in [1] or _s == 0:
                if _s == 0:
                    _P.append((n, _r1, 1))
                    _P.append((n - 2, None, 0))
                    _s = -1
                elif _s == 1:
                    _r1 = _r
                    _s = 0
                if _s == 0:
                    _r = _r1 * n * (n - 1)
                    _s = -1
    return _r
factorial(100000)