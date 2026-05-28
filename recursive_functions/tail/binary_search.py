def binary_search(a, x, lower, upper):
    if lower > upper: # empty list
        return -1
    else:
        middle = (lower + upper) // 2

        if x == a[middle]:
            return middle
        elif x < a[middle]:
            return binary_search(a, x, lower, middle - 1)
        else:
            return binary_search(a, x, middle + 1, upper)

def binary_search_wrapper(a, x):
   return binary_search(a, x, 0, len(a) - 1)


import timeit
sizes   = [1_000, 100_000, 1_000_000]
repeats = [10_000, 1_000, 100]
for n, reps in zip(sizes, repeats):
    a = list(range(n))
    cases = [("hit",  a[n // 2]),
             ("miss", a[-1] + 1)]
    for label, x in cases:
        t = timeit.timeit(lambda: binary_search_wrapper(a, x), number=reps)
        print(f"n={n:>10}  {label}  {t / reps * 1e6:.2f} µs/call")