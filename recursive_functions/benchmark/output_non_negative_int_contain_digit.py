
def contains_digit_tail(n, d):
    while not (n < 10 or n % 10 == d):
        n, d = (n // 10, d)
    if n < 10:
        return n == d
    else:
        return True


n = int("1" * 1_000)  # pior caso: 1000 dígitos, nenhum é 2
d = 2

# --- benchmark ---
def chamada():
    return contains_digit_tail(n, d)
