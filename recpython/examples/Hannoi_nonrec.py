def Hannoi(n, a, b, c):
    _P = []
    _P.append((n, a, b, c, None, None, 0))
    while len(_P) > 0:
        n, a, b, c, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [1, 2] or (_s == 0 and n > 0):
            if _s == 0:
                _P.append((n, a, b, c, _r1, _r2, 1))
                _P.append((n - 1, a, c, b, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r1
            if _s == 0:
                print(f'{a} => {b}')
            if _s == 0:
                _P.append((n, a, b, c, _r1, _r2, 2))
                _P.append((n - 1, b, c, a, None, None, 0))
                _s = -1
            elif _s == 2:
                _r2 = _r
                _s = 0
            if _s == 0:
                _r2
    return _r
for i in range(20):
    Hannoi(i, 'A', 'B', 'C')