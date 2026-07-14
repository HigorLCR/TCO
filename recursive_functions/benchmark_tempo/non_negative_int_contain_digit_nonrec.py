def contains_digit_tail(n, d):
    _P = []
    _P.append((n, d, None, 0))
    while len(_P) > 0:
        n, d, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n < 10):
            if _s == 0:
                _r = n == d
                _s = -1
        elif _s in [1] or _s == 0:
            if _s in [] or (_s == 0 and n % 10 == d):
                if _s == 0:
                    _r = True
                    _s = -1
            elif _s in [1] or _s == 0:
                if _s == 0:
                    _P.append((n, d, _r1, 1))
                    _P.append((n // 10, d, None, 0))
                    _s = -1
                elif _s == 1:
                    _r1 = _r
                    _s = 0
                if _s == 0:
                    _r = _r1
                    _s = -1
    return _r

import timeit

n = int("1" * 1_000)  # pior caso: 1000 dígitos, nenhum é 2
d = 2


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: contains_digit_tail(n, d))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
