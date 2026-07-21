
def Hannoi(n, a, b, c):
	if n > 0:
		Hannoi(n-1, a, c, b)
		print(f'{a} => {b}')
		Hannoi(n-1, b, c, a)


n = 10

# --- benchmark ---
def chamada():
    return Hannoi(n, 'A', 'B', 'C')
