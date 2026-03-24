def gcd1(m, n):
    if m == 0:
        return n
    elif m > n:
        return gcd1(n, m)
    else:
        return gcd1(m, n - m)