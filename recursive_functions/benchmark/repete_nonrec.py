import sys
import timeit
from collections.abc import Callable
sys.setrecursionlimit(10000)

def repete[**P](f: Callable[P, None], n: int, args: tuple, kwargs: dict) -> None:
    _P = []
    _P.append((f, n, args, kwargs, None, 0))
    while len(_P) > 0:
        f, n, args, kwargs, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n <= 0):
            if _s == 0:
                _r = None
                _s = -1
        if _s == 0:
            f(*args, **kwargs)
        if _s == 0:
            _P.append((f, n, args, kwargs, _r1, 1))
            _P.append((f, n - 1, args, kwargs, None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            _r1
    return _r

def _noop(*args, **kwargs):
    pass
n = 1000
qtd_execucoes = 1000
tempo = timeit.timeit(lambda: repete(_noop, n, ('x',), {}), number=qtd_execucoes)
print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')