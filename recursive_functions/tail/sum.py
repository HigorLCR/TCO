def tail_sum(list, n, s):
    if n == 0:
        return n
    else:
        return tail_sum(list, n-1, s+list[n])