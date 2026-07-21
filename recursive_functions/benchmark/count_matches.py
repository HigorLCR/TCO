import sys

sys.setrecursionlimit(10_000)


def count_matches(lst, target, acc=0):
    if not lst:
        return acc
    else:
        return count_matches(
            lst[1:],
            target,
            acc + (1 if lst[0] == target else 0)
        )


n = 1_000
lst = [1, 2, 3] * (n // 3)
target = 2

# --- benchmark ---
def chamada():
    return count_matches(lst, target)
