import sys

sys.setrecursionlimit(10_000)

# Cobre o no TypeVar (PEP 695): funcao recursiva generica sobre o tipo T.


def tamanho[T](lst: list[T]) -> int:
    if not lst:
        return 0
    return 1 + tamanho(lst[1:])


data = list(range(1_000))

# --- benchmark ---
def chamada():
    return tamanho(data)
