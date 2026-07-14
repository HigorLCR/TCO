import os
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
qtd_execucoes = 100000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (T e piso: itera ate somar >= T s).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(lambda: fast_pow(base, exp), number=qtd_execucoes)
    print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: fast_pow(base, exp))
    _k, _e = 0, 0.0                        # iteracoes completas, tempo somado
    _lote = 1
    while _e < _T:                         # T e piso: so para ao alcanca-lo
        _e += _bench.timeit(number=_lote)
        _k += _lote
        if _e >= _T:
            break
        _est = int((_T - _e) / (_e / _k))  # estimativa do que falta pela taxa
        _lote = max(1, min(_est, _lote * 10))
    print(f"benchmark por tempo (piso {_T}s): {_k} iteracoes | {_e:.4f}s total | {_e/_k*1000:.4f}ms por chamada")
