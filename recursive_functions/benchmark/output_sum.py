def Sum_Rec(L, n, acc=0):
    while not n == 0:
        L, n, acc = (L, n - 1, acc + L[n - 1])
    return acc

N = [1 for i in range(10000)]

import timeit
qtd_execucoes = 1000
tempo = timeit.timeit(
    lambda: Sum_Rec(N, 10000),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")