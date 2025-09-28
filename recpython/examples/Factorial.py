import sys
sys.setrecursionlimit(100000)  # Aumenta o limite para 3000 chamadas

def factorial(n):
    if n == 0:
        return 1
    elif n == 1:
        return 1
    else:
        return factorial(n-2) * n * (n-1)
    

factorial(100000)
