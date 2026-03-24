def linear_search_tail(a, x):
    n = len(a)
    if a == []:
        return -1
    elif a[n - 1] == x:
        return n - 1
    else:
        return linear_search_tail(a[:n - 1], x)