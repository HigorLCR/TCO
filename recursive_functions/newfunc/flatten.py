from typing import Any
import timeit


def flatten(lst, acc=None):
    if acc is None:
        acc = []
    if not lst:
        return acc
    head, *tail = lst
    if isinstance(head, list):
        return flatten(head + tail, acc)
    return flatten(tail, acc + [head])


def _placeholder() -> Any:
    pass


qtd_execucoes = 10_000
tempo = timeit.timeit(
    lambda: flatten([[i, [i + 1]] for i in range(0, 20, 2)]),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
