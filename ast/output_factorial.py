
def tail_factorial(n, a):
    while not n == 0:
        n, a = (n - 1, n * a)
    return a

tail_factorial(50000, 1)