def tail_factorial(n, a):
    while not n == 0:
        n, a = (n - 1, n * a)
    return a

n1 = 5000
n2 = 1

import timeit
qtd_execucoes = 100
tempo = timeit.timeit(
    lambda: tail_factorial(n1, n2),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")