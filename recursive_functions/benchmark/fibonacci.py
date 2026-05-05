import sys
sys.setrecursionlimit(10000000)

def tail_fibonacci(n, a=1, b=1):
    if n == 1:
        return a
    elif n == 2:
        return b
    else:
        return tail_fibonacci(n - 1, b, a + b)


tail_fibonacci(500000)