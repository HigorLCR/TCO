def linear_search_tail(a, x):
    n = len(a)
    if a == []:
        return -1
    elif a[n - 1] == x:
        return n - 1
    else:
        return linear_search_tail(a[:n - 1], x)

import sys
import timeit

sys.setrecursionlimit(1_500)

n = 1_000
a = list(range(n))
x = -1  # pior caso: elemento não encontrado
qtd_execucoes = 1_000

tempo = timeit.timeit(lambda: linear_search_tail(a, x), number=qtd_execucoes)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")