import sys
import timeit

sys.setrecursionlimit(10_000)

# Cobre os nos Set (literal {0}) e SetComp ({i for i in ...}).
# Versao SEM yield (a original usava yield -> nao transformavel pelo recpython3).
# A chamada recursiva fica FORA da comprehension, entao a SetComp nao contem
# recursao e o transformador a deixa intacta.


def countdown(n):
    if n <= 0:
        return {0}                       # Set (literal)
    nivel = {i for i in range(n)}        # SetComp
    return nivel | countdown(n - 1)


data = 200

qtd_execucoes = 1_000
tempo = timeit.timeit(
    lambda: countdown(data),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
