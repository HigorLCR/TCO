def Sum_Rec(L, n):
    _P = []
    _P.append((L, n, None, None, 0))
    while len(_P) > 0:
        L, n, res, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n == 0):
            if _s == 0:
                _r = 0
                _s = -1
        elif _s in [1] or _s == 0:
            if _s == 0:
                _P.append((L, n, res, _r1, 1))
                _P.append((L, n - 1, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                res = _r1 + L[n - 1]
            if _s == 0:
                _r = res
                _s = -1
    return _r
N = [5000000] * 1
f = Sum_Rec
for n in N:
    L = [2 for i in range(n)]
    f(L, n)
print(f(L, n))