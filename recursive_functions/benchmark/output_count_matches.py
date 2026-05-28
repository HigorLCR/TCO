import timeit


def count_matches(lst, target, acc=0):
    while not not lst:
        lst, target, acc = (lst[1:], target, acc + (1 if lst[0] == target else 0))
    return acc


n = 1_000
lst = [1, 2, 3] * (n // 3)
target = 2

qtd_execucoes = 1_000
tempo = timeit.timeit(
    lambda: count_matches(lst, target),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
