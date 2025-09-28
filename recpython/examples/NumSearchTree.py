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

for n in range(18):
	print(NumArvBusca(n))