import math
import os
import sys
import timeit

sys.setrecursionlimit(10000)

def sum_nested(data):
    _P = []
    _P.append((data, None, None, None, 0))
    while len(_P) > 0:
        data, _r1, _r2, _r3, _s = _P.pop()
        if _s == 0:
            _r = None
        match data:
            case None | False:
                if _s == 0:
                    _r = 0
                    _s = -1
            case math.inf:
                if _s == 0:
                    _r = 0
                    _s = -1
            case int(n):
                if _s == 0:
                    _r = n
                    _s = -1
            case []:
                if _s == 0:
                    _r = 0
                    _s = -1
            case [head, *tail]:
                if _s == 0:
                    _P.append((data, _r1, _r2, _r3, 1))
                    _P.append((head, None, None, None, 0))
                    _s = -1
                elif _s == 1:
                    _r1 = _r
                    _s = 0
                if _s == 0:
                    _P.append((data, _r1, _r2, _r3, 2))
                    _P.append((tail, None, None, None, 0))
                    _s = -1
                elif _s == 2:
                    _r2 = _r
                    _s = 0
                if _s == 0:
                    _r = _r1 + _r2
                    _s = -1
            case {'value': v}:
                if _s == 0:
                    _P.append((data, _r1, _r2, _r3, 3))
                    _P.append((v, None, None, None, 0))
                    _s = -1
                elif _s == 3:
                    _r3 = _r
                    _s = 0
                if _s == 0:
                    _r = _r3
                    _s = -1
            case _ as unknown:
                if _s == 0:
                    _r = 0
                    _s = -1
    return _r
nested = [1, [2, [3, 4]], [5, 6], {'value': 7}, None, False]
qtd_execucoes = 100000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(lambda: sum_nested(nested), number=qtd_execucoes)
    print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: sum_nested(nested))
    _ncal, _tcal = _bench.autorange()      # calibra: lote com _tcal >= 0.2s
    if _tcal >= _T:
        _k, _e = _ncal, _tcal              # a calibracao ja cobriu a duracao
    else:
        _alvo = max(1, round(_T / (_tcal / _ncal)))
        _e = _bench.timeit(number=_alvo)   # roda ~T segundos
        _k = _alvo
    _execucoes = _k * (_T / _e)            # normaliza para exatamente T
    print(f"execucoes em {_T}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
