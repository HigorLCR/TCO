import os
import timeit

def count_bits(n, acc=0):
    _P = []
    _P.append((n, acc, None, 0))
    while len(_P) > 0:
        n, acc, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n == 0):
            if _s == 0:
                _r = acc
                _s = -1
        elif _s in [1] or _s == 0:
            if _s == 0:
                _P.append((n, acc, _r1, 1))
                _P.append((n >> 1, acc + (n & 1), None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r = _r1
                _s = -1
    return _r
mask = 255
n = 255
a = n | mask
b = n ^ mask
c = n << 2
d = ~n
n_pos = +n
results = []
for i in range(100):
    if i % 2 == 0:
        continue
    results.append(count_bits(i))
n = (1 << 20) - 1
qtd_execucoes = 100000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (T e piso: itera ate somar >= T s).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(lambda: count_bits(n), number=qtd_execucoes)
    print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: count_bits(n))
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
