import os
import sys
import timeit

sys.setrecursionlimit(10_000)

# Cobre o no MatMult (operador @): potencia de matriz por recursao,
# M @ M @ ... @ M. A classe Matriz implementa @ via __matmul__ (Python puro,
# sem numpy). So a funcao 'potencia' e recursiva; o __matmul__ nao e tocado
# pelo recpython3 (nao tem auto-chamada).


class Matriz:
    def __init__(self, dados):
        self.dados = dados

    def __matmul__(self, outra):
        a, b = self.dados, outra.dados
        n, comum, p = len(a), len(b), len(b[0])
        produto = [
            [sum(a[i][k] * b[k][j] for k in range(comum)) for j in range(p)]
            for i in range(n)
        ]
        return Matriz(produto)


def potencia(m, n):
    if n == 1:
        return m
    return m @ potencia(m, n - 1)


base = Matriz([[1, 1], [0, 1]])
expoente = 500

qtd_execucoes = 1_000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(
        lambda: potencia(base, expoente),
        number=qtd_execucoes
    )
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: potencia(base, expoente))
    _ncal, _tcal = _bench.autorange()      # calibra: lote com _tcal >= 0.2s
    if _tcal >= _T:
        _k, _e = _ncal, _tcal              # a calibracao ja cobriu a duracao
    else:
        _alvo = max(1, round(_T / (_tcal / _ncal)))
        _e = _bench.timeit(number=_alvo)   # roda ~T segundos
        _k = _alvo
    _execucoes = _k * (_T / _e)            # normaliza para exatamente T
    print(f"execucoes em {_T}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
