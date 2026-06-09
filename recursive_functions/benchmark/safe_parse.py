import sys
import timeit

sys.setrecursionlimit(10_000)

_error_count = 0


def safe_parse(lst, acc=None):
    global _error_count
    if acc is None:
        acc = []
    if not lst:
        return acc
    try:
        val = int(lst[0])
    except (ValueError, TypeError):
        val = None
        _error_count += 1
    return safe_parse(lst[1:], acc + [val])


data = ['1', 'abc', '3', None, '5'] * 200

qtd_execucoes = 1_000
tempo = timeit.timeit(
    lambda: safe_parse(data),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
