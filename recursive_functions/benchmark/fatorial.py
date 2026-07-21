import sys

sys.setrecursionlimit(10_000)

def fatorial(n):
    if n <= 1:
        return 1
    return n * fatorial(n - 1)


n = 1_000

# --- benchmark ---
def chamada():
    return fatorial(n)
