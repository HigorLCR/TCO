def contains_digit_tail(n, d):
    if n < 10:
        return n == d
    elif n % 10 == d:
        return True
    else:
        return contains_digit_tail(n // 10, d)