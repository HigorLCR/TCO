import timeit


def count_bits(n, acc=0):
    if n == 0:
        return acc
    else:
        return count_bits(n >> 1, acc + (n & 1))


mask = 0xFF
n = 255
a = n | mask
b = n ^ mask
c = n << 2
d = ~n
n_pos = +n

results = []
for i in range(100):
    if i % 2 == 0:
        continue
    results.append(count_bits(i))

n = (1 << 20) - 1

qtd_execucoes = 100_000
tempo = timeit.timeit(
    lambda: count_bits(n),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
