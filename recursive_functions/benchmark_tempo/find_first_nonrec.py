import sys
import timeit
from typing import Callable
sys.setrecursionlimit(100000)

def find_first(lst: list, pred: Callable, idx: int=0):
    _P = []
    _P.append((lst, pred, idx, None, None, 0))
    while len(_P) > 0:
        lst, pred, idx, val, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and idx >= len(lst)):
            if _s == 0:
                _r = None
                _s = -1
        elif _s in [1] or _s == 0:
            if _s in [] or (_s == 0 and pred((val := lst[idx]))):
                if _s == 0:
                    _r = val
                    _s = -1
            elif _s in [1] or _s == 0:
                if _s == 0:
                    _P.append((lst, pred, idx, val, _r1, 1))
                    _P.append((lst, pred, idx + 1, None, None, 0))
                    _s = -1
                elif _s == 1:
                    _r1 = _r
                    _s = 0
                if _s == 0:
                    _r = _r1
                    _s = -1
    return _r
n = 1000
lst = list(range(n))
pred = lambda x: x > 5000


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: find_first(lst, pred))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
