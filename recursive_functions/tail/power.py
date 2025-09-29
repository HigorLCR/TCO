def tail_power(base, exponent, accumulator=1):
    if exponent == 0:
        return accumulator
    else:
        # Recursão tail: toda a computação acontece antes da chamada recursiva
        return tail_power(base, exponent - 1, accumulator * base)