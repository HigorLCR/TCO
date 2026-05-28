import sys
import timeit

sys.setrecursionlimit(100_000)


def fast_pow(base, exp, acc=1):
    if exp < 0:
        raise ValueError(f"expoente deve ser não-negativo, recebeu {exp}")
    if exp == 0:
        return acc
    elif exp % 2 != 0:
        return fast_pow(base, exp - 1, acc * base)
    else:
        return fast_pow(base * base, exp // 2, acc)


result: int = fast_pow(2, 10)
assert fast_pow(2, 10) == 2 ** 10
assert fast_pow(3, 5) == 3 ** 5
assert fast_pow(7, 0) == 1

base = 2
exp = 10_000

i = 0
while i < 20:
    if fast_pow(2, i) != 2 ** i:
        break
    i += 1

qtd_execucoes = 100_000
tempo = timeit.timeit(
    lambda: fast_pow(base, exp),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
