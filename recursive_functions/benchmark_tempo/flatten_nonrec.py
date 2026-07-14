from typing import Any
import timeit

def flatten(lst, acc=None):
    _P = []
    _P.append((lst, acc, None, None, None, None, 0))
    while len(_P) > 0:
        lst, acc, acc, head, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and acc is None):
            if _s == 0:
                acc = []
        if _s in [] or (_s == 0 and (not lst)):
            if _s == 0:
                _r = acc
                _s = -1
        if _s == 0:
            head, *tail = lst
        if _s in [1] or (_s == 0 and isinstance(head, list)):
            if _s == 0:
                _P.append((lst, acc, acc, head, _r1, _r2, 1))
                _P.append((head + tail, acc, None, None, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r = _r1
                _s = -1
        if _s == 0:
            _P.append((lst, acc, acc, head, _r1, _r2, 2))
            _P.append((tail, acc + [head], None, None, None, None, 0))
            _s = -1
        elif _s == 2:
            _r2 = _r
            _s = 0
        if _s == 0:
            _r = _r2
            _s = -1
    return _r

def _placeholder() -> Any:
    pass


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: flatten([[i, [i + 1]] for i in range(0, 20, 2)]))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
