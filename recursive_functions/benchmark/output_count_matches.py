
def count_matches(lst, target, acc=0):
    while not not lst:
        lst, target, acc = (lst[1:], target, acc + (1 if lst[0] == target else 0))
    return acc


n = 1_000
lst = [1, 2, 3] * (n // 3)
target = 2

# --- benchmark ---
def chamada():
    return count_matches(lst, target)
