import sys

sys.setrecursionlimit(10_000)

# Cobre o no TypeVarTuple (PEP 695): type param *Ts numa funcao recursiva.
# Caso "forcado": tuple[*Ts] modela aridade fixa, mas a recursao com t[1:]
# muda a aridade a cada passo -- a anotacao deixa de valer semanticamente.


def conta[*Ts](t: tuple[*Ts]) -> int:
    if not t:
        return 0
    return 1 + conta(t[1:])


data = tuple(range(1_000))

# --- benchmark ---
def chamada():
    return conta(data)
