import sys

sys.setrecursionlimit(10000)

def soma_trystar(n):
    _P = []
    _P.append((n, None, None, 0))
    while len(_P) > 0:
        n, parcial, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n <= 0):
            if _s == 0:
                _r = 0
                _s = -1
        if _s == 0:
            parcial = 0
        try:
            raise ExceptionGroup('grupo', [ValueError(n)])
        except* ValueError:
            if _s == 0:
                _P.append((n, parcial, _r1, 1))
                _P.append((n - 1, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                parcial = n + _r1
        if _s == 0:
            _r = parcial
            _s = -1
    return _r
data = 500

# --- benchmark ---
def chamada():
    return soma_trystar(data)
