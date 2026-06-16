import sys

sys.setrecursionlimit(100000)

n1 = 5000
n2 = 1

def tail_factorial(n, a):
    if n == 0: 
        return a
    else:
        return tail_factorial(n-1, n*a)



import timeit
qtd_execucoes = 100
tempo = timeit.timeit(
    lambda: tail_factorial(n1, n2),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")

