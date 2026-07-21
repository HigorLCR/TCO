
def linear_search_tail(a, x):
    n = len(a)
    while not (a == [] or a[n - 1] == x):
        a, x = (a[:n - 1], x)
        n = len(a)
    if a == []:
        return -1
    else:
        return n - 1


n = 1_000
a = list(range(n))
x = -1  # pior caso: elemento não encontrado

# --- benchmark ---
def chamada():
    return linear_search_tail(a, x)
