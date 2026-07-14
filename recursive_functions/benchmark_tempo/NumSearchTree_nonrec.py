def NumArvBusca(n):
    _P = []
    _P.append((n, None, None, None, None, None, None, None, 0))
    while len(_P) > 0:
        n, s, _, r, _for1, _for2, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n == 0):
            if _s == 0:
                _r = 1
                _s = -1
        elif _s in [1, 2] or _s == 0:
            if _s == 0:
                s = 0
            if _s == 0:
                _for2 = iter(range(1, n + 1))
            while _s in [1, 2] or (_s == 0 and True):
                try:
                    if _s == 0:
                        r = next(_for2)
                    if _s == 0:
                        _P.append((n, s, _, r, _for1, _for2, _r1, _r2, 1))
                        _P.append((r - 1, None, None, None, None, None, None, None, 0))
                        _s = -1
                    elif _s == 1:
                        _r1 = _r
                        _s = 0
                    if _s == 0:
                        _P.append((n, s, _, r, _for1, _for2, _r1, _r2, 2))
                        _P.append((n - r, None, None, None, None, None, None, None, 0))
                        _s = -1
                    elif _s == 2:
                        _r2 = _r
                        _s = 0
                    if _s == 0:
                        _for1 = iter(range(_r1 * _r2))
                    while _s in [1, 2] or (_s == 0 and True):
                        try:
                            if _s == 0:
                                _ = next(_for1)
                            if _s == 0:
                                s += 1
                        except StopIteration:
                            break
                except StopIteration:
                    break
            if _s == 0:
                _r = s
                _s = -1
    return _r
import timeit

n = 12


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: NumArvBusca(n))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
