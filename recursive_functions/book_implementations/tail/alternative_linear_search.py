def linear_search_tail_alt(a, x, index):
    if a == []:
        return -1
    elif a[0] == x:
        return index
    else:
        return linear_search_tail_alt(a[1:], x, index + 1)


def linear_search_alt_tail_wrapper(a, x):
    return linear_search_tail_alt(a, x, 0)