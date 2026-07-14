import timeit

def fib_memo(n, memo=None):
    _P = []
    _P.append((n, memo, None, None, None, 0))
    while len(_P) > 0:
        n, memo, memo, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and memo is None):
            if _s == 0:
                memo = {}
        if _s in [] or (_s == 0 and n in memo):
            if _s == 0:
                _r = memo[n]
                _s = -1
        if _s in [] or (_s == 0 and n <= 1):
            if _s == 0:
                _r = n
                _s = -1
        if _s == 0:
            _P.append((n, memo, memo, _r1, _r2, 1))
            _P.append((n - 1, memo, None, None, None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            _P.append((n, memo, memo, _r1, _r2, 2))
            _P.append((n - 2, memo, None, None, None, 0))
            _s = -1
        elif _s == 2:
            _r2 = _r
            _s = 0
        if _s == 0:
            memo[n] = _r1 + _r2
        if _s == 0:
            _r = memo[n]
            _s = -1
    return _r

def fib_with_counter(n):
    count = 0
    cache = {}

    def _fib(k):
        _P = []
        _P.append((k, None, None, 0))
        while len(_P) > 0:
            k, _r1, _r2, _s = _P.pop()
            if _s == 0:
                _r = None
            nonlocal count
            if _s == 0:
                count += 1
            if _s in [] or (_s == 0 and k in cache):
                if _s == 0:
                    _r = cache[k]
                    _s = -1
            if _s in [] or (_s == 0 and k <= 1):
                if _s == 0:
                    _r = k
                    _s = -1
            if _s == 0:
                _P.append((k, _r1, _r2, 1))
                _P.append((k - 1, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _P.append((k, _r1, _r2, 2))
                _P.append((k - 2, None, None, 0))
                _s = -1
            elif _s == 2:
                _r2 = _r
                _s = 0
            if _s == 0:
                cache[k] = _r1 + _r2
            if _s == 0:
                _r = cache[k]
                _s = -1
        return _r
    return (_fib(n), count)
warm_cache = {k: fib_memo(k) for k in range(20)}
n = 35


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: fib_memo(n))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
