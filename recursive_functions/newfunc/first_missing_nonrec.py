import sys
import timeit
sys.setrecursionlimit(10000)

def first_missing(lst, candidate=0):
    _P = []
    _P.append((lst, candidate, None, 0))
    while len(_P) > 0:
        lst, candidate, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and candidate not in lst):
            if _s == 0:
                _r = candidate
                _s = -1
        elif _s in [1] or _s == 0:
            if _s == 0:
                _P.append((lst, candidate, _r1, 1))
                _P.append((lst, candidate + 1, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r = _r1
                _s = -1
    return _r
n = 500
lst = list(range(n))
qtd_execucoes = 1000
tempo = timeit.timeit(lambda: first_missing(lst), number=qtd_execucoes)
print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')