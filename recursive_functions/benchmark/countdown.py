import os
import sys
import timeit

sys.setrecursionlimit(10_000)

# Cobre os nos Set (literal {0}) e SetComp ({i for i in ...}).
# Versao SEM yield (a original usava yield -> nao transformavel pelo recpython3).
# A chamada recursiva fica FORA da comprehension, entao a SetComp nao contem
# recursao e o transformador a deixa intacta.


def countdown(n):
    if n <= 0:
        return {0}                       # Set (literal)
    nivel = {i for i in range(n)}        # SetComp
    return nivel | countdown(n - 1)


data = 200

qtd_execucoes = 1_000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (T e piso: itera ate somar >= T s).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(
        lambda: countdown(data),
        number=qtd_execucoes
    )
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: countdown(data))
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
