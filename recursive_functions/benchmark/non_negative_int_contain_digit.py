def contains_digit_tail(n, d):
    if n < 10:
        return n == d
    elif n % 10 == d:
        return True
    else:
        return contains_digit_tail(n // 10, d)

import sys
import timeit

sys.setrecursionlimit(1_500)

n = int("1" * 1_000)  # pior caso: 1000 dígitos, nenhum é 2
d = 2
qtd_execucoes = 1_000

tempo = timeit.timeit(lambda: contains_digit_tail(n, d), number=qtd_execucoes)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")