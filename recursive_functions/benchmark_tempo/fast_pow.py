import sys
import timeit

sys.setrecursionlimit(100_000)


def fast_pow(base, exp, acc=1):
    if exp < 0:
        raise ValueError(f"expoente deve ser não-negativo, recebeu {exp}")
    if exp == 0:
        return acc
    elif exp % 2 != 0:
        return fast_pow(base, exp - 1, acc * base)
    else:
        return fast_pow(base * base, exp // 2, acc)


result: int = fast_pow(2, 10)
assert fast_pow(2, 10) == 2 ** 10
assert fast_pow(3, 5) == 3 ** 5
assert fast_pow(7, 0) == 1

base = 2
exp = 10_000

i = 0
while i < 20:
    if fast_pow(2, i) != 2 ** i:
        break
    i += 1


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: fast_pow(base, exp))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
