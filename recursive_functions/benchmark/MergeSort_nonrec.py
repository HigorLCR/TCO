import os
import timeit

def MergeSort_Rec(L, i, j):
    _P = []
    _P.append((L, i, j, None, None, None, 0))
    while len(_P) > 0:
        L, i, j, m, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None

        def Merge(L, i, m, j):
            Ln = []
            p1 = i
            p2 = m + 1
            for _ in range(j - i + 1):
                if p2 > j or (p1 <= m and L[p1] < L[p2]):
                    Ln.append(L[p1])
                    p1 += 1
                else:
                    Ln.append(L[p2])
                    p2 += 1
            for k in range(j - i + 1):
                L[i + k] = Ln[k]
        if _s in [1, 2] or (_s == 0 and i < j):
            if _s == 0:
                m = (i + j) // 2
            if _s == 0:
                _P.append((L, i, j, m, _r1, _r2, 1))
                _P.append((L, i, m, None, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r1
            if _s == 0:
                _P.append((L, i, j, m, _r1, _r2, 2))
                _P.append((L, m + 1, j, None, None, None, 0))
                _s = -1
            elif _s == 2:
                _r2 = _r
                _s = 0
            if _s == 0:
                _r2
            if _s == 0:
                Merge(L, i, m, j)
    return _r

n = 1_000
qtd_execucoes = 1_000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(lambda: MergeSort_Rec(list(range(n, 0, -1)), 0, n - 1), number=qtd_execucoes)
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: MergeSort_Rec(list(range(n, 0, -1)), 0, n - 1))
    _ncal, _tcal = _bench.autorange()      # calibra: lote com _tcal >= 0.2s
    if _tcal >= _T:
        _k, _e = _ncal, _tcal              # a calibracao ja cobriu a duracao
    else:
        _alvo = max(1, round(_T / (_tcal / _ncal)))
        _e = _bench.timeit(number=_alvo)   # roda ~T segundos
        _k = _alvo
    _execucoes = _k * (_T / _e)            # normaliza para exatamente T
    print(f"execucoes em {_T}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
