import os
import timeit

def woodcutter(t, wood, lower, upper):
    _P = []
    _P.append((t, wood, lower, upper, None, None, None, None, 0))
    while len(_P) > 0:
        t, wood, lower, upper, middle_h, wood_collected, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s == 0:
            middle_h = (lower + upper) // 2
        if _s == 0:
            wood_collected = sum((max(0, tree - middle_h) for tree in t))
        if _s in [] or (_s == 0 and (wood_collected == wood or lower == upper)):
            if _s == 0:
                _r = middle_h
                _s = -1
        elif _s in [1, 2] or _s == 0:
            if _s in [] or (_s == 0 and lower == upper - 1):
                if _s in [] or (_s == 0 and sum((max(0, tree - upper) for tree in t)) >= wood):
                    if _s == 0:
                        _r = upper
                        _s = -1
                elif _s in [] or _s == 0:
                    if _s == 0:
                        _r = lower
                        _s = -1
            elif _s in [1, 2] or _s == 0:
                if _s in [1] or (_s == 0 and wood_collected > wood):
                    if _s == 0:
                        _P.append((t, wood, lower, upper, middle_h, wood_collected, _r1, _r2, 1))
                        _P.append((t, wood, middle_h, upper, None, None, None, None, 0))
                        _s = -1
                    elif _s == 1:
                        _r1 = _r
                        _s = 0
                    if _s == 0:
                        _r = _r1
                        _s = -1
                elif _s in [2] or _s == 0:
                    if _s == 0:
                        _P.append((t, wood, lower, upper, middle_h, wood_collected, _r1, _r2, 2))
                        _P.append((t, wood, lower, middle_h - 1, None, None, None, None, 0))
                        _s = -1
                    elif _s == 2:
                        _r2 = _r
                        _s = 0
                    if _s == 0:
                        _r = _r2
                        _s = -1
    return _r


arvores = list(range(1, 100001))
madeira = 1250025000
altura_minima = 0
altura_maxima = max(arvores)

qtd_execucoes = 100


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(
        lambda: woodcutter(arvores, madeira, altura_minima, altura_maxima),
        number=qtd_execucoes
    )
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: woodcutter(arvores, madeira, altura_minima, altura_maxima))
    _ncal, _tcal = _bench.autorange()      # calibra: lote com _tcal >= 0.2s
    if _tcal >= _T:
        _k, _e = _ncal, _tcal              # a calibracao ja cobriu a duracao
    else:
        _alvo = max(1, round(_T / (_tcal / _ncal)))
        _e = _bench.timeit(number=_alvo)   # roda ~T segundos
        _k = _alvo
    _execucoes = _k * (_T / _e)            # normaliza para exatamente T
    print(f"execucoes em {_T}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
