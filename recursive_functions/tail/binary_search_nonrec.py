def binary_search(a, x, lower, upper):
    _P = []
    _P.append((a, x, lower, upper, None, None, None, 0))
    while len(_P) > 0:
        a, x, lower, upper, middle, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and lower > upper):
            if _s == 0:
                _r = -1
                _s = -1
        elif _s in [1, 2] or _s == 0:
            if _s == 0:
                middle = (lower + upper) // 2
            if _s in [] or (_s == 0 and x == a[middle]):
                if _s == 0:
                    _r = middle
                    _s = -1
            elif _s in [1, 2] or _s == 0:
                if _s in [1] or (_s == 0 and x < a[middle]):
                    if _s == 0:
                        _P.append((a, x, lower, upper, middle, _r1, _r2, 1))
                        _P.append((a, x, lower, middle - 1, None, None, None, 0))
                        _s = -1
                    elif _s == 1:
                        _r1 = _r
                        _s = 0
                    if _s == 0:
                        _r = _r1
                        _s = -1
                elif _s in [2] or _s == 0:
                    if _s == 0:
                        _P.append((a, x, lower, upper, middle, _r1, _r2, 2))
                        _P.append((a, x, middle + 1, upper, None, None, None, 0))
                        _s = -1
                    elif _s == 2:
                        _r2 = _r
                        _s = 0
                    if _s == 0:
                        _r = _r2
                        _s = -1
    return _r

def binary_search_wrapper(a, x):
    return binary_search(a, x, 0, len(a) - 1)