def Hannoi(n, a, b, c):
	if n > 0:
		Hannoi(n-1, a, c, b)
		print(f'{a} => {b}')
		Hannoi(n-1, b, c, a)

for i in range(20):
	Hannoi(i, "A", "B", "C")