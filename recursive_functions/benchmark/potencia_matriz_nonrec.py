import sys

sys.setrecursionlimit(10000)

class Matriz:

    def __init__(self, dados):
        self.dados = dados

    def __matmul__(self, outra):
        a, b = (self.dados, outra.dados)
        n, comum, p = (len(a), len(b), len(b[0]))
        produto = [[sum((a[i][k] * b[k][j] for k in range(comum))) for j in range(p)] for i in range(n)]
        return Matriz(produto)

def potencia(m, n):
    _P = []
    _P.append((m, n, None, 0))
    while len(_P) > 0:
        m, n, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and n == 1):
            if _s == 0:
                _r = m
                _s = -1
        if _s == 0:
            _P.append((m, n, _r1, 1))
            _P.append((m, n - 1, None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            _r = m @ _r1
            _s = -1
    return _r
base = Matriz([[1, 1], [0, 1]])
expoente = 500

# --- benchmark ---
def chamada():
    return potencia(base, expoente)
