import os
import sys
import timeit

sys.setrecursionlimit(10_000)

# Cobre o no TryStar (try/except*, PEP 654). Caso FORCADO: nao se pode dar
# 'return' dentro de um bloco except* (SyntaxError), entao a recursao acontece
# numa atribuicao dentro do handler e o 'return' fica fora. Levanta um
# ExceptionGroup so para ter o que tratar com except*.


def soma_trystar(n):
    if n <= 0:
        return 0
    parcial = 0
    try:
        raise ExceptionGroup("grupo", [ValueError(n)])
    except* ValueError:
        parcial = n + soma_trystar(n - 1)
    return parcial


data = 500

qtd_execucoes = 1_000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(
        lambda: soma_trystar(data),
        number=qtd_execucoes
    )
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: soma_trystar(data))
    _ncal, _tcal = _bench.autorange()      # calibra: lote com _tcal >= 0.2s
    if _tcal >= _T:
        _k, _e = _ncal, _tcal              # a calibracao ja cobriu a duracao
    else:
        _alvo = max(1, round(_T / (_tcal / _ncal)))
        _e = _bench.timeit(number=_alvo)   # roda ~T segundos
        _k = _alvo
    _execucoes = _k * (_T / _e)            # normaliza para exatamente T
    print(f"execucoes em {_T}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
