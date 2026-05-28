def tail_fibonacci(n, a=1, b=1):
    while not (n == 1 or n == 2):
        n, a, b = (n - 1, b, a + b)
    if n == 1:
        return a
    else:
        return b
    
tail_fibonacci(500000)


import timeit
qtd_execucoes = 100
tempo = timeit.timeit(
    lambda: tail_fibonacci(500000),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")