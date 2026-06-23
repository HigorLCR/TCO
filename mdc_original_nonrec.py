def mdc(a, b):
    _P = []
    _P.append((a, b, None, None, None, 0))
    while len(_P) > 0:
        a, b, a, b, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s == 0:
            a = a
        if _s == 0:
            b = b
        if _s in [] or (_s == 0 and b == 0):
            if _s == 0:
                _r = a
                _s = -1
        elif _s in [1] or _s == 0:
            if _s == 0:
                _P.append((a, b, a, b, _r1, 1))
                _P.append((b, a % b, None, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r = _r1
                _s = -1
    return _r
print(mdc(48, 18))