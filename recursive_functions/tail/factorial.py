import sys

sys.setrecursionlimit(100000)

n1 = 50000
n2 = 1

def tail_factorial(n, a):
    if n == 0: 
        return a
    else:
        return tail_factorial(n-1, n*a)

tail_factorial(n1, n2)

