def linear_search_tail(a, x):
    _P = []
    _P.append((a, x, None, None, 0))
    while len(_P) > 0:
        a, x, n, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s == 0:
            n = len(a)
        if _s in [] or (_s == 0 and a == []):
            if _s == 0:
                _r = -1
                _s = -1
        elif _s in [1] or _s == 0:
            if _s in [] or (_s == 0 and a[n - 1] == x):
                if _s == 0:
                    _r = n - 1
                    _s = -1
            elif _s in [1] or _s == 0:
                if _s == 0:
                    _P.append((a, x, n, _r1, 1))
                    _P.append((a[:n - 1], x, None, None, 0))
                    _s = -1
                elif _s == 1:
                    _r1 = _r
                    _s = 0
                if _s == 0:
                    _r = _r1
                    _s = -1
    return _r

import timeit

n = 1_000
a = list(range(n))
x = -1  # pior caso: elemento não encontrado
qtd_execucoes = 1_000

tempo = timeit.timeit(lambda: linear_search_tail(a, x), number=qtd_execucoes)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")