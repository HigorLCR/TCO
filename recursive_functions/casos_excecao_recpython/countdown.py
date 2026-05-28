import sys
import timeit

sys.setrecursionlimit(10_000)


def countdown(n):
    if n < 0:
        return
    yield n
    yield from countdown(n - 1)


seen = {0, 1, 2}
evens = {x for x in range(100) if x % 2 == 0}

n = 500

qtd_execucoes = 10_000
tempo = timeit.timeit(
    lambda: list(countdown(n)),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
