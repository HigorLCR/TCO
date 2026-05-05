def tail_fibonacci(n, a=1, b=1):
    while not (n == 1 or n == 2):
        n, a, b = (n - 1, b, a + b)
    if n == 1:
        return a
    else:
        return b
    
tail_fibonacci(1000000)