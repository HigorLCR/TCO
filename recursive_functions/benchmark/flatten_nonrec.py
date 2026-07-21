from typing import Any

def flatten(lst, acc=None):
    _P = []
    _P.append((lst, acc, None, None, None, None, 0))
    while len(_P) > 0:
        lst, acc, acc, head, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and acc is None):
            if _s == 0:
                acc = []
        if _s in [] or (_s == 0 and (not lst)):
            if _s == 0:
                _r = acc
                _s = -1
        if _s == 0:
            head, *tail = lst
        if _s in [1] or (_s == 0 and isinstance(head, list)):
            if _s == 0:
                _P.append((lst, acc, acc, head, _r1, _r2, 1))
                _P.append((head + tail, acc, None, None, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r = _r1
                _s = -1
        if _s == 0:
            _P.append((lst, acc, acc, head, _r1, _r2, 2))
            _P.append((tail, acc + [head], None, None, None, None, 0))
            _s = -1
        elif _s == 2:
            _r2 = _r
            _s = 0
        if _s == 0:
            _r = _r2
            _s = -1
    return _r

def _placeholder() -> Any:
    pass

# --- benchmark ---
def chamada():
    return flatten([[i, [i + 1]] for i in range(0, 20, 2)])
