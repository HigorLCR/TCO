def linear_search_tail(a, x):
    n = len(a)
    while not (a == [] or a[n - 1] == x):
        a, x = (a[:n - 1], x)
        n = len(a)
    if a == []:
        return -1
    else:
        return n - 1

import timeit

n = 1_000
a = list(range(n))
x = -1  # pior caso: elemento não encontrado
qtd_execucoes = 1_000

tempo = timeit.timeit(lambda: linear_search_tail(a, x), number=qtd_execucoes)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")