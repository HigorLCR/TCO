import sys
import timeit

sys.setrecursionlimit(10_000)

# Cobre o no TypeVar (PEP 695): funcao recursiva generica sobre o tipo T.


def tamanho[T](lst: list[T]) -> int:
    if not lst:
        return 0
    return 1 + tamanho(lst[1:])


data = list(range(1_000))

qtd_execucoes = 1_000
tempo = timeit.timeit(
    lambda: tamanho(data),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
