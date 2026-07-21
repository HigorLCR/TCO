import sys

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

# --- benchmark ---
def chamada():
    return soma_trystar(data)
