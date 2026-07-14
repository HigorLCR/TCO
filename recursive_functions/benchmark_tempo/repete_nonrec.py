import sys
import timeit
from collections.abc import Callable
sys.setrecursionlimit(10000)

def repete[**P](f: Callable[P, None], n: int, args: tuple, kwargs: dict) -> None:
    _P = []
    _P.append((f, n, args, kwargs, None, 0))
    while len(_P) > 0:
        f, n, args, kwargs, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n <= 0):
            if _s == 0:
                _r = None
                _s = -1
        if _s == 0:
            f(*args, **kwargs)
        if _s == 0:
            _P.append((f, n, args, kwargs, _r1, 1))
            _P.append((f, n - 1, args, kwargs, None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            _r1
    return _r

def _noop(*args, **kwargs):
    pass
n = 1000


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: repete(_noop, n, ('x',), {}))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
