
def tail_gcd(a, b):
    a, b = abs(a), abs(b)
    
    def gcd_helper(a, b):
        # Caso base
        if b == 0:
            return a
        else:
            # Recursão tail: toda a computação acontece antes da chamada recursiva
            return gcd_helper(b, a % b)
    
    return gcd_helper(a, b)


def tail_mdc(a, b, c):
    a, b = abs(a), abs(b)

    if b == 0:
        return a
    else:
        return tail_mdc(b, a % b, c)