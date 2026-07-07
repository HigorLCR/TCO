import sys
import timeit

sys.setrecursionlimit(10_000)

# Cobre o no TryStar (try/except*, PEP 654). Caso FORCADO: nao se pode dar
# 'return' dentro de um bloco except* (SyntaxError), entao a recursao acontece
# numa atribuicao dentro do handler e o 'return' fica fora. Levanta um
# ExceptionGroup so para ter o que tratar com except*.


def soma_trystar(n):
    if n <= 0:
        return 0
    parcial = 0
    try:
        raise ExceptionGroup("grupo", [ValueError(n)])
    except* ValueError:
        parcial = n + soma_trystar(n - 1)
    return parcial


data = 500

qtd_execucoes = 1_000
tempo = timeit.timeit(
    lambda: soma_trystar(data),
    number=qtd_execucoes
)
print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
