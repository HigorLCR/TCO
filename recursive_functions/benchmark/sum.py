import sys
sys.setrecursionlimit(10000000)

def Sum_Rec(L, n, acc = 0):
	if n == 0:
		return acc
	else:
		return Sum_Rec(L, n-1, acc + L[n-1])
	
N = [1 for i in range(5000000)];


import timeit
qtd_execucoes = 100
tempo = timeit.timeit(
    lambda: Sum_Rec(N, 5000000),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")