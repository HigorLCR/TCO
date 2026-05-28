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