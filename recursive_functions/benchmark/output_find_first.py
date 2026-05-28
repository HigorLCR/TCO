import timeit
from typing import Callable


def find_first(lst: list, pred: Callable, idx: int=0):
    while not (idx >= len(lst) or pred((val := lst[idx]))):
        lst, pred, idx = (lst, pred, idx + 1)
    if idx >= len(lst):
        return None
    else:
        return val


n = 10_00
lst = list(range(n))
pred = lambda x: x > 5_000

qtd_execucoes = 10_00
tempo = timeit.timeit(
    lambda: find_first(lst, pred),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
