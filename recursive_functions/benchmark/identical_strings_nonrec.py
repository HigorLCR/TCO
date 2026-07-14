import os
import timeit

def equal_strings_tail(s, t):
    _P = []
    _P.append((s, t, None, 0))
    while len(_P) > 0:
        s, t, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and len(s) != len(t)):
            if _s == 0:
                _r = False
                _s = -1
        elif _s in [1] or _s == 0:
            if _s in [] or (_s == 0 and s == ''):
                if _s == 0:
                    _r = True
                    _s = -1
            elif _s in [1] or _s == 0:
                if _s in [] or (_s == 0 and s[0] != t[0]):
                    if _s == 0:
                        _r = False
                        _s = -1
                elif _s in [1] or _s == 0:
                    if _s == 0:
                        _P.append((s, t, _r1, 1))
                        _P.append((s[1:], t[1:], None, 0))
                        _s = -1
                    elif _s == 1:
                        _r1 = _r
                        _s = 0
                    if _s == 0:
                        _r = _r1
                        _s = -1
    return _r


n = 10_000
s = "a" * n  # pior caso: strings idênticas forçam iteração até o fim
t = s
qtd_execucoes = 1_000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(lambda: equal_strings_tail(s, t), number=qtd_execucoes)
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: equal_strings_tail(s, t))
    _ncal, _tcal = _bench.autorange()      # calibra: lote com _tcal >= 0.2s
    if _tcal >= _T:
        _k, _e = _ncal, _tcal              # a calibracao ja cobriu a duracao
    else:
        _alvo = max(1, round(_T / (_tcal / _ncal)))
        _e = _bench.timeit(number=_alvo)   # roda ~T segundos
        _k = _alvo
    _execucoes = _k * (_T / _e)            # normaliza para exatamente T
    print(f"execucoes em {_T}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
