def equal_strings_tail(s, t):
    _P = []
    _P.append((s, t, None, 0))
    while len(_P) > 0:
        s, t, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and len(s) != len(t)):
            if _s == 0:
                _r = False
                _s = -1
        elif _s in [1] or _s == 0:
            if _s in [] or (_s == 0 and s == ''):
                if _s == 0:
                    _r = True
                    _s = -1
            elif _s in [1] or _s == 0:
                if _s in [] or (_s == 0 and s[0] != t[0]):
                    if _s == 0:
                        _r = False
                        _s = -1
                elif _s in [1] or _s == 0:
                    if _s == 0:
                        _P.append((s, t, _r1, 1))
                        _P.append((s[1:], t[1:], None, 0))
                        _s = -1
                    elif _s == 1:
                        _r1 = _r
                        _s = 0
                    if _s == 0:
                        _r = _r1
                        _s = -1
    return _r