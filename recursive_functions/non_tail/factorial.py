def factorial(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return factorial(n-2) * n * (n-1)