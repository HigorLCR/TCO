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


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: potencia(base, expoente))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
