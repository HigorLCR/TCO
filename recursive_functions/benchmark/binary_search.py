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

n = 1_000_000
a = list(range(n))
qtd_execucoes = 1000

x = a[-1] + 1  # pior caso: elemento não encontrado

tempo = timeit.timeit(lambda: binary_search_wrapper(a, x), number=qtd_execucoes)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
