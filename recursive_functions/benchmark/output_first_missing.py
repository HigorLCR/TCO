
def first_missing(lst, candidate=0):
    while not candidate not in lst:
        lst, candidate = (lst, candidate + 1)
    return candidate


n = 500
lst = list(range(n))

# --- benchmark ---
def chamada():
    return first_missing(lst)
