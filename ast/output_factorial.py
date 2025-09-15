def tail_factorial(n, a):
    while not n == 0:
        b = 1
        for i in range(1, n + 1):
            b *= i
            print('B: ', b)
        n, a = (n - 1, n * a)
    c = True
    if not c:
        print('A: ', a)
    return a

print(tail_factorial(5, 1))