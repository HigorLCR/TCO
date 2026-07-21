import sys

def contains_digit_tail(n, d):
    if n < 10:
        return n == d
    elif n % 10 == d:
        return True
    else:
        return contains_digit_tail(n // 10, d)


sys.setrecursionlimit(1_500)

n = int("1" * 1_000)  # pior caso: 1000 dígitos, nenhum é 2
d = 2

# --- benchmark ---
def chamada():
    return contains_digit_tail(n, d)
