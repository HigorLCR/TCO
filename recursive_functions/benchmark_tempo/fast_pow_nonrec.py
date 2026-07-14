import sys
import timeit
sys.setrecursionlimit(100000)

def fast_pow(base, exp, acc=1):
    _P = []
    _P.append((base, exp, acc, None, None, 0))
    while len(_P) > 0:
        base, exp, acc, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and exp < 0):
            raise ValueError(f'expoente deve ser não-negativo, recebeu {exp}')
        if _s in [] or (_s == 0 and exp == 0):
            if _s == 0:
                _r = acc
                _s = -1
        elif _s in [1, 2] or _s == 0:
            if _s in [1] or (_s == 0 and exp % 2 != 0):
                if _s == 0:
                    _P.append((base, exp, acc, _r1, _r2, 1))
                    _P.append((base, exp - 1, acc * base, None, None, 0))
                    _s = -1
                elif _s == 1:
                    _r1 = _r
                    _s = 0
                if _s == 0:
                    _r = _r1
                    _s = -1
            elif _s in [2] or _s == 0:
                if _s == 0:
                    _P.append((base, exp, acc, _r1, _r2, 2))
                    _P.append((base * base, exp // 2, acc, None, None, 0))
                    _s = -1
                elif _s == 2:
                    _r2 = _r
                    _s = 0
                if _s == 0:
                    _r = _r2
                    _s = -1
    return _r
result: int = fast_pow(2, 10)
assert fast_pow(2, 10) == 2 ** 10
assert fast_pow(3, 5) == 3 ** 5
assert fast_pow(7, 0) == 1
base = 2
exp = 10000
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
