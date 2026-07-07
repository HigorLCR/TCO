import sys
import timeit

sys.setrecursionlimit(10_000)

def fatorial(n):
    if n <= 1:
        return 1
    return n * fatorial(n - 1)


n = 1_000

qtd_execucoes = 1_000
tempo = timeit.timeit(
    lambda: fatorial(n),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
