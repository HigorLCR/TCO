def woodcutter(t, wood, lower, upper):
    middle_h = (lower + upper) // 2
    wood_collected = sum(max(0, tree - middle_h) for tree in t)

    if wood_collected == wood or lower == upper:
        return middle_h
    elif lower == upper - 1:
        if sum(max(0, tree - upper) for tree in t) >= wood:
            return upper
        else:
            return lower
    elif wood_collected > wood:
        return woodcutter(t, wood, middle_h, upper)
 


import timeit

arvores = list(range(1, 100001))
madeira = 1250025000
altura_minima = 0
altura_maxima = max(arvores)

qtd_execucoes = 100
tempo = timeit.timeit(
    lambda: woodcutter(arvores, madeira, altura_minima, altura_maxima),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada") 