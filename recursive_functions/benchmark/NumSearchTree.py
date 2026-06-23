def NumArvBusca(n):
	if n == 0:
		return 1
	else:
		s = 0
		for r in range(1,n+1):
			for _ in range(NumArvBusca(r-1) * NumArvBusca(n - r)):
				s += 1
			#print(f"n={n} r={r} s={s}")
		return s

import timeit

n = 12
qtd_execucoes = 100

tempo = timeit.timeit(lambda: NumArvBusca(n), number=qtd_execucoes)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")