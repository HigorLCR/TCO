import sys
import timeit
from collections.abc import Callable

sys.setrecursionlimit(10_000)

# Cobre o no ParamSpec (PEP 695): o no vem do [**P] nos type_params, e P captura
# a assinatura de f via Callable[P, None].
# Para ser compativel com o recpython3, os argumentos de f sao passados como
# parametros NORMAIS (args: tuple, kwargs: dict) -> a chamada recursiva tem
# aridade FIXA. O unpacking *args/**kwargs ocorre so na chamada a f, que NAO e
# recursiva (logo o transformador nao mexe nela).


def repete[**P](f: Callable[P, None], n: int, args: tuple, kwargs: dict) -> None:
    if n <= 0:
        return None
    f(*args, **kwargs)
    repete(f, n - 1, args, kwargs)


def _noop(*args, **kwargs):
    pass


n = 1_000


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: repete(_noop, n, ("x",), {}))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
