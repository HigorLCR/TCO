def contains_digit_tail(n, d):
    _P = []
    _P.append((n, d, None, 0))
    while len(_P) > 0:
        n, d, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n < 10):
            if _s == 0:
                _r = n == d
                _s = -1
        elif _s in [1] or _s == 0:
            if _s in [] or (_s == 0 and n % 10 == d):
                if _s == 0:
                    _r = True
                    _s = -1
            elif _s in [1] or _s == 0:
                if _s == 0:
                    _P.append((n, d, _r1, 1))
                    _P.append((n // 10, d, None, 0))
                    _s = -1
                elif _s == 1:
                    _r1 = _r
                    _s = 0
                if _s == 0:
                    _r = _r1
                    _s = -1
    return _r

import timeit

n = int("1" * 1_000)  # pior caso: 1000 dígitos, nenhum é 2
d = 2
qtd_execucoes = 1_000

tempo = timeit.timeit(lambda: contains_digit_tail(n, d), number=qtd_execucoes)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")