import sys
sys.setrecursionlimit(10000000)

def Sum_Rec(L, n, acc=0):
    _P = []
    _P.append((L, n, acc, None, 0))
    while len(_P) > 0:
        L, n, acc, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n == 0):
            if _s == 0:
                _r = acc
                _s = -1
        elif _s in [1] or _s == 0:
            if _s == 0:
                _P.append((L, n, acc, _r1, 1))
                _P.append((L, n - 1, acc + L[n - 1], None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r = _r1
                _s = -1
    return _r
N = [1 for i in range(5000000)]
import timeit
qtd_execucoes = 100
tempo = timeit.timeit(
    lambda: Sum_Rec(N, 5000000),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")