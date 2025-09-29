def tail_sum(list, n, s):
    while not n == 0:
        list, n, s = (list, n - 1, s + list[n])
    return n