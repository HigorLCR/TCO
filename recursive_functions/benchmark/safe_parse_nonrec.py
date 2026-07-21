import sys

sys.setrecursionlimit(10000)
_error_count = 0

def safe_parse(lst, acc=None):
    _P = []
    _P.append((lst, acc, None, None, None, 0))
    while len(_P) > 0:
        lst, acc, acc, val, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        global _error_count
        if _s in [] or (_s == 0 and acc is None):
            if _s == 0:
                acc = []
        if _s in [] or (_s == 0 and (not lst)):
            if _s == 0:
                _r = acc
                _s = -1
        try:
            if _s == 0:
                val = int(lst[0])
        except (ValueError, TypeError):
            if _s == 0:
                val = None
            if _s == 0:
                _error_count += 1
        if _s == 0:
            _P.append((lst, acc, acc, val, _r1, 1))
            _P.append((lst[1:], acc + [val], None, None, None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            _r = _r1
            _s = -1
    return _r
data = ['1', 'abc', '3', None, '5'] * 200

# --- benchmark ---
def chamada():
    return safe_parse(data)
