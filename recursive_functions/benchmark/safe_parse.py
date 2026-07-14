import os
import sys
import timeit

sys.setrecursionlimit(10_000)

_error_count = 0


def safe_parse(lst, acc=None):
    global _error_count
    if acc is None:
        acc = []
    if not lst:
        return acc
    try:
        val = int(lst[0])
    except (ValueError, TypeError):
        val = None
        _error_count += 1
    return safe_parse(lst[1:], acc + [val])


data = ['1', 'abc', '3', None, '5'] * 200

qtd_execucoes = 1_000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(
        lambda: safe_parse(data),
        number=qtd_execucoes
    )
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: safe_parse(data))
    _ncal, _tcal = _bench.autorange()      # calibra: lote com _tcal >= 0.2s
    if _tcal >= _T:
        _k, _e = _ncal, _tcal              # a calibracao ja cobriu a duracao
    else:
        _alvo = max(1, round(_T / (_tcal / _ncal)))
        _e = _bench.timeit(number=_alvo)   # roda ~T segundos
        _k = _alvo
    _execucoes = _k * (_T / _e)            # normaliza para exatamente T
    print(f"execucoes em {_T}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
