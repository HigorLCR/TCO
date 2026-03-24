def linear_search_linear(a, x, n):
    if a == []:
        return -1
    elif a[0] == x:
        return 0
    else:
        return 1 + linear_search_linear(a[1:], x, n)


def linear_search_linear_wrapper(a, x):
    return linear_search_linear(a, x, len(a))