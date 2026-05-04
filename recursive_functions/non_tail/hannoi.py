def hannoi(n, a, b, c):
	if n > 0:
		hannoi(n-1, a, c, b)
		print(f'{a} => {b}')
		hannoi(n-1, b, c, a)

for i in range(20):
	hannoi(i, "A", "B", "C")