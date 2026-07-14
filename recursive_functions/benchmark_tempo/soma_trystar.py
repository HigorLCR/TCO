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


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: soma_trystar(data))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
