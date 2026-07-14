import os
import random
import sys
import timeit

def quickselect(a, lower, upper, k):
    if lower == upper:
        return a[lower]
    else:
        pivot_index = partition_Hoare_wrapper(a, lower, upper)

        if pivot_index == k - 1:
            return a[pivot_index]
        elif pivot_index < k - 1:
            return quickselect(a, pivot_index + 1, upper, k)
        else:
            return quickselect(a, lower, pivot_index - 1, k)

def partition_Hoare_rec(a, left, right, pivot):
    if left > right:
        return right
    else:
        if a[left] > pivot and a[right] <= pivot:
            aux = a[left]
            a[left] = a[right]
            a[right] = aux
            return partition_Hoare_rec(a, left + 1, right - 1, pivot)
        else:
            if a[left] <= pivot:
                left = left + 1
            if a[right] > pivot:
                right = right - 1
            return partition_Hoare_rec(a, left, right, pivot)

def partition_Hoare_wrapper(a, lower, upper):
    if upper >= 0:
        middle = (lower + upper) // 2
        pivot = a[middle]
        a[middle] = a[lower]
        a[lower] = pivot

        right = partition_Hoare_rec(a, lower + 1, upper, pivot)

        a[lower] = a[right]
        a[right] = pivot

        return right
    

sys.setrecursionlimit(10_000)

random.seed(42)
n = 10_000
a_orig = list(range(n))
random.shuffle(a_orig)
k = n // 2  # pior caso: mediana
qtd_execucoes = 1_000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(
        lambda: quickselect(a_orig[:], 0, n - 1, k), 
        number=qtd_execucoes
    )
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: quickselect(a_orig[:], 0, n - 1, k))
    _ncal, _tcal = _bench.autorange()      # calibra: lote com _tcal >= 0.2s
    if _tcal >= _T:
        _k, _e = _ncal, _tcal              # a calibracao ja cobriu a duracao
    else:
        _alvo = max(1, round(_T / (_tcal / _ncal)))
        _e = _bench.timeit(number=_alvo)   # roda ~T segundos
        _k = _alvo
    _execucoes = _k * (_T / _e)            # normaliza para exatamente T
    print(f"execucoes em {_T}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
