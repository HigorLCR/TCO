import sys
import timeit
sys.setrecursionlimit(10000)

def fatorial(n):
    _P = []
    _P.append((n, None, 0))
    while len(_P) > 0:
        n, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n <= 1):
            if _s == 0:
                _r = 1
                _s = -1
        if _s == 0:
            _P.append((n, _r1, 1))
            _P.append((n - 1, None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            _r = n * _r1
            _s = -1
    return _r
n = 1000
qtd_execucoes = 1000
tempo = timeit.timeit(lambda: fatorial(n), number=qtd_execucoes)
print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')