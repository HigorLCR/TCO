
def count_bits(n, acc=0):
    while not n == 0:
        n, acc = (n >> 1, acc + (n & 1))
    return acc


n = (1 << 20) - 1

# --- benchmark ---
def chamada():
    return count_bits(n)
