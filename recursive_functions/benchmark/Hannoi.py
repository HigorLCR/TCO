def Hannoi(n, a, b, c):
	if n > 0:
		Hannoi(n-1, a, c, b)
		print(f'{a} => {b}')
		Hannoi(n-1, b, c, a)

import timeit

n = 10
qtd_execucoes = 1000

tempo = timeit.timeit(lambda: Hannoi(n, 'A', 'B', 'C'), number=qtd_execucoes)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")