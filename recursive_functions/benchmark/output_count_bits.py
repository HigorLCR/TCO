import timeit


def count_bits(n, acc=0):
    while not n == 0:
        n, acc = (n >> 1, acc + (n & 1))
    return acc


n = (1 << 20) - 1

qtd_execucoes = 100_000
tempo = timeit.timeit(
    lambda: count_bits(n),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
