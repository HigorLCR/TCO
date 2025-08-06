def tail_factorial(n, a):
    if n == 0:
        return a
    else:
        return tail_factorial(n-1, n*a)