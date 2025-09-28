def NumArvBusca(n):
    _P = []
    _P.append((n, None, None, None, None, None, None, None, 0))
    while len(_P) > 0:
        n, s, _, r, _for1, _for2, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n == 0):
            if _s == 0:
                _r = 1
                _s = -1
        elif _s in [1, 2] or _s == 0:
            if _s == 0:
                s = 0
            if _s == 0:
                _for2 = iter(range(1, n + 1))
            while _s in [1, 2] or (_s == 0 and True):
                try:
                    if _s == 0:
                        r = next(_for2)
                    if _s == 0:
                        _P.append((n, s, _, r, _for1, _for2, _r1, _r2, 1))
                        _P.append((r - 1, None, None, None, None, None, None, None, 0))
                        _s = -1
                    elif _s == 1:
                        _r1 = _r
                        _s = 0
                    if _s == 0:
                        _P.append((n, s, _, r, _for1, _for2, _r1, _r2, 2))
                        _P.append((n - r, None, None, None, None, None, None, None, 0))
                        _s = -1
                    elif _s == 2:
                        _r2 = _r
                        _s = 0
                    if _s == 0:
                        _for1 = iter(range(_r1 * _r2))
                    while _s in [1, 2] or (_s == 0 and True):
                        try:
                            if _s == 0:
                                _ = next(_for1)
                            if _s == 0:
                                s += 1
                        except StopIteration:
                            break
                except StopIteration:
                    break
            if _s == 0:
                _r = s
                _s = -1
    return _r
for n in range(18):
    print(NumArvBusca(n))