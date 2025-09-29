def tail_mdc(a, b, c):
    while not b == 0:
        a, b = (abs(a), abs(b))
        a, b, c = (b, a % b, c)
    a, b = (abs(a), abs(b))
    return a