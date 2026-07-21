import sys

sys.setrecursionlimit(100000)

def fast_pow(base, exp, acc=1):
    _P = []
    _P.append((base, exp, acc, None, None, 0))
    while len(_P) > 0:
        base, exp, acc, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and exp < 0):
            raise ValueError(f'expoente deve ser não-negativo, recebeu {exp}')
        if _s in [] or (_s == 0 and exp == 0):
            if _s == 0:
                _r = acc
                _s = -1
        elif _s in [1, 2] or _s == 0:
            if _s in [1] or (_s == 0 and exp % 2 != 0):
                if _s == 0:
                    _P.append((base, exp, acc, _r1, _r2, 1))
                    _P.append((base, exp - 1, acc * base, None, None, 0))
                    _s = -1
                elif _s == 1:
                    _r1 = _r
                    _s = 0
                if _s == 0:
                    _r = _r1
                    _s = -1
            elif _s in [2] or _s == 0:
                if _s == 0:
                    _P.append((base, exp, acc, _r1, _r2, 2))
                    _P.append((base * base, exp // 2, acc, None, None, 0))
                    _s = -1
                elif _s == 2:
                    _r2 = _r
                    _s = 0
                if _s == 0:
                    _r = _r2
                    _s = -1
    return _r
result: int = fast_pow(2, 10)
assert fast_pow(2, 10) == 2 ** 10
assert fast_pow(3, 5) == 3 ** 5
assert fast_pow(7, 0) == 1
base = 2
exp = 10000
i = 0
while i < 20:
    if fast_pow(2, i) != 2 ** i:
        break
    i += 1

# --- benchmark ---
def chamada():
    return fast_pow(base, exp)
