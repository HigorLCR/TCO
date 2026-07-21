import sys

sys.setrecursionlimit(10_000)


def first_missing(lst, candidate=0):
    if candidate not in lst:
        return candidate
    else:
        return first_missing(lst, candidate + 1)


n = 500
lst = list(range(n))

# --- benchmark ---
def chamada():
    return first_missing(lst)
