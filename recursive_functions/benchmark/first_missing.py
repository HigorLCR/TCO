import sys
import timeit

sys.setrecursionlimit(10_000)


def first_missing(lst, candidate=0):
    if candidate not in lst:
        return candidate
    else:
        return first_missing(lst, candidate + 1)


n = 500
lst = list(range(n))

qtd_execucoes = 1_000
tempo = timeit.timeit(
    lambda: first_missing(lst),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
