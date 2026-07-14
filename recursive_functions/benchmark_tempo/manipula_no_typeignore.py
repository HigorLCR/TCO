import sys
import timeit
import ast

sys.setrecursionlimit(10_000)

# Funcao recursiva que manipula nos ast.TypeIgnore.
# O TypeIgnore representa um comentario "# type: ignore" e SO existe quando o
# codigo e parseado com type_comments=True, ficando em Module.type_ignores
# (nunca como filho de um statement). Por isso ele nunca aparece num parse
# padrao nem no ast.walk de um arquivo comum -- assim como os nos de mod
# (Interactive/Expression/FunctionType), a cobertura aqui e DEMONSTRATIVA:
# a funcao constroi e manipula os nos em tempo de execucao.
#
# TypeIgnore nao tem nos-filhos (campos: lineno:int, tag:str), entao a recursao
# analoga e sobre a LISTA de type_ignores: processa o no do indice atual e
# recursa no proximo, acumulando uma NOVA lista com os linenos deslocados.


def desloca_type_ignores(ignores, offset, i, acc):
    """Devolve uma nova lista de ast.TypeIgnore com lineno deslocado por offset.

    Recursao de cauda sobre os indices (i, i+1, ...), compativel com o recpython.
    - i >= len: caso base, devolve o acumulador.
    - ast.TypeIgnore: manipula o no, somando offset ao lineno e mantendo a tag.
    """
    if i >= len(ignores):
        return acc
    no = ignores[i]
    novo = ast.TypeIgnore(lineno=no.lineno + offset, tag=no.tag)
    acc.append(novo)
    return desloca_type_ignores(ignores, offset, i + 1, acc)


# Entrada do benchmark: muitos "# type: ignore" parseados com type_comments=True,
# de onde extraimos a lista de nos ast.TypeIgnore (Module.type_ignores).
quantidade = 1_000
linhas = []
for j in range(quantidade):
    linhas.append(f"v{j} = {j}  # type: ignore")
codigo = "\n".join(linhas)
ignores = ast.parse(codigo, type_comments=True).type_ignores


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: desloca_type_ignores(ignores, 1_000, 0, []))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
