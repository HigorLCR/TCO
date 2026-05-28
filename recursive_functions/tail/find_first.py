import sys
import timeit
from typing import Callable

sys.setrecursionlimit(100_000)


def find_first(lst: list, pred: Callable, idx: int = 0):
    if idx >= len(lst):
        return None
    elif pred(val := lst[idx]):
        return val
    else:
        return find_first(lst, pred, idx + 1)


n = 10_00
lst = list(range(n))
pred = lambda x: x > 5_000

qtd_execucoes = 10_00
tempo = timeit.timeit(
    lambda: find_first(lst, pred),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
