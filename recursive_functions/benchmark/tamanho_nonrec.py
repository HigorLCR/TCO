import sys
import timeit
sys.setrecursionlimit(10000)

def tamanho[T](lst: list[T]) -> int:
    _P = []
    _P.append((lst, None, 0))
    while len(_P) > 0:
        lst, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and (not lst)):
            if _s == 0:
                _r = 0
                _s = -1
        if _s == 0:
            _P.append((lst, _r1, 1))
            _P.append((lst[1:], None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            _r = 1 + _r1
            _s = -1
    return _r
data = list(range(1000))
qtd_execucoes = 1000
tempo = timeit.timeit(lambda: tamanho(data), number=qtd_execucoes)
print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')