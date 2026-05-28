def quickselect(a, lower, upper, k):
    _P = []
    _P.append((a, lower, upper, k, None, None, None, 0))
    while len(_P) > 0:
        a, lower, upper, k, pivot_index, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and lower == upper):
            if _s == 0:
                _r = a[lower]
                _s = -1
        elif _s in [1, 2] or _s == 0:
            if _s == 0:
                pivot_index = partition_Hoare_wrapper(a, lower, upper)
            if _s in [] or (_s == 0 and pivot_index == k - 1):
                if _s == 0:
                    _r = a[pivot_index]
                    _s = -1
            elif _s in [1, 2] or _s == 0:
                if _s in [1] or (_s == 0 and pivot_index < k - 1):
                    if _s == 0:
                        _P.append((a, lower, upper, k, pivot_index, _r1, _r2, 1))
                        _P.append((a, pivot_index + 1, upper, k, None, None, None, 0))
                        _s = -1
                    elif _s == 1:
                        _r1 = _r
                        _s = 0
                    if _s == 0:
                        _r = _r1
                        _s = -1
                elif _s in [2] or _s == 0:
                    if _s == 0:
                        _P.append((a, lower, upper, k, pivot_index, _r1, _r2, 2))
                        _P.append((a, lower, pivot_index - 1, k, None, None, None, 0))
                        _s = -1
                    elif _s == 2:
                        _r2 = _r
                        _s = 0
                    if _s == 0:
                        _r = _r2
                        _s = -1
    return _r

def partition_Hoare_rec(a, left, right, pivot):
    _P = []
    _P.append((a, left, right, pivot, None, None, None, None, None, 0))
    while len(_P) > 0:
        a, left, right, pivot, aux, _lc, _rc, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and left > right):
            if _s == 0:
                _r = right
                _s = -1
        elif _s in [1, 2] or _s == 0:
            if _s in [1] or (_s == 0 and (a[left] > pivot and a[right] <= pivot)):
                if _s == 0:
                    aux = a[left]
                if _s == 0:
                    a[left] = a[right]
                if _s == 0:
                    a[right] = aux
                if _s == 0:
                    _P.append((a, left, right, pivot, aux, left, right, _r1, _r2, 1))
                    _P.append((a, left + 1, right - 1, pivot, None, None, None, None, None, 0))
                    _s = -1
                elif _s == 1:
                    _r1 = _r
                    _s = 0
                if _s == 0:
                    _r = _r1
                    _s = -1
            elif _s in [2] or _s == 0:
                if _s in [] or (_s == 0 and a[left] <= pivot):
                    if _s == 0:
                        left = left + 1
                if _s in [] or (_s == 0 and a[right] > pivot):
                    if _s == 0:
                        right = right - 1
                if _s == 0:
                    _P.append((a, left, right, pivot, aux, left, right, _r1, _r2, 2))
                    _P.append((a, left, right, pivot, None, None, None, None, None, 0))
                    _s = -1
                elif _s == 2:
                    _r2 = _r
                    _s = 0
                if _s == 0:
                    _r = _r2
                    _s = -1
    return _r

def partition_Hoare_wrapper(a, lower, upper):
    if upper >= 0:
        middle = (lower + upper) // 2
        pivot = a[middle]
        a[middle] = a[lower]
        a[lower] = pivot
        right = partition_Hoare_rec(a, lower + 1, upper, pivot)
        a[lower] = a[right]
        a[right] = pivot
        return right