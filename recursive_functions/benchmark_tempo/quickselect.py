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
    

import sys
import timeit
import random

sys.setrecursionlimit(10_000)

random.seed(42)
n = 10_000
a_orig = list(range(n))
random.shuffle(a_orig)
k = n // 2  # pior caso: mediana


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: quickselect(a_orig[:], 0, n - 1, k))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
