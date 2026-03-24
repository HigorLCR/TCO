def contains_digit(n, d):
    if n < 10:
        return n == d
    else:
        return (n % 10 == d) or contains_digit(n // 10, d)