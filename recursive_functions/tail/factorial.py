import sys

sys.setrecursionlimit(100000)

def tail_factorial(n, a):
    if n == 0: 
        return a
    else:
        return tail_factorial(n-1, n*a)

tail_factorial(50000, 1)