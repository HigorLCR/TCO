import os
import timeit

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


n = 1_000
a = list(range(n))
x = -1  # pior caso: elemento não encontrado
qtd_execucoes = 1_000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (T e piso: itera ate somar >= T s).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(lambda: linear_search_tail(a, x), number=qtd_execucoes)
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: linear_search_tail(a, x))
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
