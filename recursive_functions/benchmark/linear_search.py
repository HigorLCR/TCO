import sys

def linear_search_tail(a, x):
    n = len(a)
    if a == []:
        return -1
    elif a[n - 1] == x:
        return n - 1
    else:
        return linear_search_tail(a[:n - 1], x)


sys.setrecursionlimit(1_500)

n = 1_000
a = list(range(n))
x = -1  # pior caso: elemento não encontrado

# --- benchmark ---
def chamada():
    return linear_search_tail(a, x)
