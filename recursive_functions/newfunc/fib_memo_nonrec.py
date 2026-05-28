import timeit

def fib_memo(n, memo=None):
    _P = []
    _P.append((n, memo, None, None, None, 0))
    while len(_P) > 0:
        n, memo, memo, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and memo is None):
            if _s == 0:
                memo = {}
        if _s in [] or (_s == 0 and n in memo):
            if _s == 0:
                _r = memo[n]
                _s = -1
        if _s in [] or (_s == 0 and n <= 1):
            if _s == 0:
                _r = n
                _s = -1
        if _s == 0:
            _P.append((n, memo, memo, _r1, _r2, 1))
            _P.append((n - 1, memo, None, None, None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            _P.append((n, memo, memo, _r1, _r2, 2))
            _P.append((n - 2, memo, None, None, None, 0))
            _s = -1
        elif _s == 2:
            _r2 = _r
            _s = 0
        if _s == 0:
            memo[n] = _r1 + _r2
        if _s == 0:
            _r = memo[n]
            _s = -1
    return _r

def fib_with_counter(n):
    count = 0
    cache = {}

    def _fib(k):
        _P = []
        _P.append((k, None, None, 0))
        while len(_P) > 0:
            k, _r1, _r2, _s = _P.pop()
            if _s == 0:
                _r = None
            nonlocal count
            if _s == 0:
                count += 1
            if _s in [] or (_s == 0 and k in cache):
                if _s == 0:
                    _r = cache[k]
                    _s = -1
            if _s in [] or (_s == 0 and k <= 1):
                if _s == 0:
                    _r = k
                    _s = -1
            if _s == 0:
                _P.append((k, _r1, _r2, 1))
                _P.append((k - 1, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _P.append((k, _r1, _r2, 2))
                _P.append((k - 2, None, None, 0))
                _s = -1
            elif _s == 2:
                _r2 = _r
                _s = 0
            if _s == 0:
                cache[k] = _r1 + _r2
            if _s == 0:
                _r = cache[k]
                _s = -1
        return _r
    return (_fib(n), count)
warm_cache = {k: fib_memo(k) for k in range(20)}
n = 35
qtd_execucoes = 1
tempo = timeit.timeit(lambda: fib_memo(n), number=qtd_execucoes)
print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')