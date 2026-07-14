import os
import timeit
from typing import Any

def flatten(lst, acc=None):
    _P = []
    _P.append((lst, acc, None, None, None, None, 0))
    while len(_P) > 0:
        lst, acc, acc, head, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and acc is None):
            if _s == 0:
                acc = []
        if _s in [] or (_s == 0 and (not lst)):
            if _s == 0:
                _r = acc
                _s = -1
        if _s == 0:
            head, *tail = lst
        if _s in [1] or (_s == 0 and isinstance(head, list)):
            if _s == 0:
                _P.append((lst, acc, acc, head, _r1, _r2, 1))
                _P.append((head + tail, acc, None, None, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r = _r1
                _s = -1
        if _s == 0:
            _P.append((lst, acc, acc, head, _r1, _r2, 2))
            _P.append((tail, acc + [head], None, None, None, None, 0))
            _s = -1
        elif _s == 2:
            _r2 = _r
            _s = 0
        if _s == 0:
            _r = _r2
            _s = -1
    return _r

def _placeholder() -> Any:
    pass
qtd_execucoes = 10000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (T e piso: itera ate somar >= T s).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(lambda: flatten([[i, [i + 1]] for i in range(0, 20, 2)]), number=qtd_execucoes)
    print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: flatten([[i, [i + 1]] for i in range(0, 20, 2)]))
    _k, _e = 0, 0.0                        # iteracoes completas, tempo somado
    _lote = 1
    while _e < _T:                         # T e piso: so para ao alcanca-lo
        _e += _bench.timeit(number=_lote)
        _k += _lote
        if _e >= _T:
            break
        _est = int((_T - _e) / (_e / _k))  # estimativa do que falta pela taxa
        _lote = max(1, min(_est, _lote * 10))
    print(f"benchmark por tempo (piso {_T}s): {_k} iteracoes | {_e:.4f}s total | {_e/_k*1000:.4f}ms por chamada")
