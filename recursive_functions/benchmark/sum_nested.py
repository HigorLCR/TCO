import math
import sys
import timeit

sys.setrecursionlimit(10_000)


def sum_nested(data):
    match data:
        case None | False:
            return 0
        case math.inf:
            return 0
        case int(n):
            return n
        case []:
            return 0
        case [head, *tail]:
            return sum_nested(head) + sum_nested(tail)
        case {"value": v}:
            return sum_nested(v)
        case _ as unknown:
            return 0


nested = [1, [2, [3, 4]], [5, 6], {"value": 7}, None, False]

qtd_execucoes = 100_000
tempo = timeit.timeit(
    lambda: sum_nested(nested),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
