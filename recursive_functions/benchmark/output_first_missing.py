import timeit


def first_missing(lst, candidate=0):
    while not candidate not in lst:
        lst, candidate = (lst, candidate + 1)
    return candidate


n = 500
lst = list(range(n))

qtd_execucoes = 1_000
tempo = timeit.timeit(
    lambda: first_missing(lst),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
