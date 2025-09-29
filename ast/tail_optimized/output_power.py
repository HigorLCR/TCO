def tail_power(base, exponent, accumulator=1):
    while not exponent == 0:
        base, exponent, accumulator = (base, exponent - 1, accumulator * base)
    return accumulator