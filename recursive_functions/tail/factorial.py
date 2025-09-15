def tail_factorial(n, a):
    if n == 0:
        c = True
        if not c:
            print("A: ", a)      
        return a
    else:
        b=1
        for i in range(1, n+1):
            b *= i
            print("B: ", b)
        return tail_factorial(n-1, n*a)