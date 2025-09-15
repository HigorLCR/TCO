def fibonacci(n):
    _p = []
    _p.append((n, None, None, 0))
    while len(_p) > 0:
        n, _r1, _r2, _s = _p.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n <= 2):
            if (_s == 0):
                _r = 1
        else:
            if _s in [1, 2] or _s == 0:
                if _s == 0:
                    _p.append((n, _r1, _r2, 1))
                    _p.append((n-1, None, None, 0))
                    _s = -1
                else:
                    if _s == 1:
                        _r1 = _r
                        _s = 0
                if _s == 0:
                    _p.append((n, _r1, _r2, 2))
                    _p.append((n-2, None, None, 0))
                    _s = -1
                else:
                    if _s == 2:
                        _r2 = _r
                        _s = 0
                if _s == 0:
                    _r = _r1 + _r2
    
    return _r

for i in range(1, 40):
    print(f"fibonacci({i}) = {fibonacci(i)}")