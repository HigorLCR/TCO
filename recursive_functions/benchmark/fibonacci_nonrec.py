import sys
sys.setrecursionlimit(10000000)

def tail_fibonacci(n, a=1, b=1):
    _P = []
    _P.append((n, a, b, None, 0))
    while len(_P) > 0:
        n, a, b, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n == 1):
            if _s == 0:
                _r = a
                _s = -1
        elif _s in [1] or _s == 0:
            if _s in [] or (_s == 0 and n == 2):
                if _s == 0:
                    _r = b
                    _s = -1
            elif _s in [1] or _s == 0:
                if _s == 0:
                    _P.append((n, a, b, _r1, 1))
                    _P.append((n - 1, b, a + b, None, 0))
                    _s = -1
                elif _s == 1:
                    _r1 = _r
                    _s = 0
                if _s == 0:
                    _r = _r1
                    _s = -1
    return _r


import timeit
qtd_execucoes = 100
tempo = timeit.timeit(
    lambda: tail_fibonacci(20000),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")