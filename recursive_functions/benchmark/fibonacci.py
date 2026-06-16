import sys
sys.setrecursionlimit(10000000)

def tail_fibonacci(n, a=1, b=1):
    if n == 1:
        return a
    elif n == 2:
        return b
    else:
        return tail_fibonacci(n - 1, b, a + b)


import timeit
qtd_execucoes = 100
tempo = timeit.timeit(
    lambda: tail_fibonacci(20000),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
