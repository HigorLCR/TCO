import os
import sys
import timeit
from typing import Callable

sys.setrecursionlimit(100000)

def find_first(lst: list, pred: Callable, idx: int=0):
    _P = []
    _P.append((lst, pred, idx, None, None, 0))
    while len(_P) > 0:
        lst, pred, idx, val, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and idx >= len(lst)):
            if _s == 0:
                _r = None
                _s = -1
        elif _s in [1] or _s == 0:
            if _s in [] or (_s == 0 and pred((val := lst[idx]))):
                if _s == 0:
                    _r = val
                    _s = -1
            elif _s in [1] or _s == 0:
                if _s == 0:
                    _P.append((lst, pred, idx, val, _r1, 1))
                    _P.append((lst, pred, idx + 1, None, None, 0))
                    _s = -1
                elif _s == 1:
                    _r1 = _r
                    _s = 0
                if _s == 0:
                    _r = _r1
                    _s = -1
    return _r
n = 1000
lst = list(range(n))
pred = lambda x: x > 5000
qtd_execucoes = 1000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(lambda: find_first(lst, pred), number=qtd_execucoes)
    print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: find_first(lst, pred))
    _ncal, _tcal = _bench.autorange()      # calibra: lote com _tcal >= 0.2s
    if _tcal >= _T:
        _k, _e = _ncal, _tcal              # a calibracao ja cobriu a duracao
    else:
        _alvo = max(1, round(_T / (_tcal / _ncal)))
        _e = _bench.timeit(number=_alvo)   # roda ~T segundos
        _k = _alvo
    _execucoes = _k * (_T / _e)            # normaliza para exatamente T
    print(f"execucoes em {_T}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
