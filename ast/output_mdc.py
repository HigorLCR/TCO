def tail_mdc(a, b, c):
    a, b = (abs(a), abs(b))
    while not b == 0:
        a, b = (abs(a), abs(b))
        a, b, c = (b, a % b, c)
    return a