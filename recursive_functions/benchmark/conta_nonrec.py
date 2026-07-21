import sys

sys.setrecursionlimit(10000)

def conta[*Ts](t: tuple[*Ts,]) -> int:
    _P = []
    _P.append((t, None, 0))
    while len(_P) > 0:
        t, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and (not t)):
            if _s == 0:
                _r = 0
                _s = -1
        if _s == 0:
            _P.append((t, _r1, 1))
            _P.append((t[1:], None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            _r = 1 + _r1
            _s = -1
    return _r
data = tuple(range(1000))

# --- benchmark ---
def chamada():
    return conta(data)
