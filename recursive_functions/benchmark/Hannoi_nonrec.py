import os
import timeit

def Hannoi(n, a, b, c):
    _P = []
    _P.append((n, a, b, c, None, None, 0))
    while len(_P) > 0:
        n, a, b, c, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [1, 2] or (_s == 0 and n > 0):
            if _s == 0:
                _P.append((n, a, b, c, _r1, _r2, 1))
                _P.append((n - 1, a, c, b, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r1
            if _s == 0:
                print(f'{a} => {b}')
            if _s == 0:
                _P.append((n, a, b, c, _r1, _r2, 2))
                _P.append((n - 1, b, c, a, None, None, 0))
                _s = -1
            elif _s == 2:
                _r2 = _r
                _s = 0
            if _s == 0:
                _r2
    return _r

n = 10
qtd_execucoes = 1000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(lambda: Hannoi(n, 'A', 'B', 'C'), number=qtd_execucoes)
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: Hannoi(n, 'A', 'B', 'C'))
    _ncal, _tcal = _bench.autorange()      # calibra: lote com _tcal >= 0.2s
    if _tcal >= _T:
        _k, _e = _ncal, _tcal              # a calibracao ja cobriu a duracao
    else:
        _alvo = max(1, round(_T / (_tcal / _ncal)))
        _e = _bench.timeit(number=_alvo)   # roda ~T segundos
        _k = _alvo
    _execucoes = _k * (_T / _e)            # normaliza para exatamente T
    print(f"execucoes em {_T}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
