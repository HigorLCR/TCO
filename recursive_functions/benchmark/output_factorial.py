
def tail_factorial(n, a):
    while not n == 0:
        n, a = (n - 1, n * a)
    return a

n1 = 5000
n2 = 1

# --- benchmark ---
def chamada():
    return tail_factorial(n1, n2)
