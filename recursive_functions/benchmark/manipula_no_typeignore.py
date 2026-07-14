import ast
import os
import sys
import timeit

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

qtd_execucoes = 1_000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(
        lambda: desloca_type_ignores(ignores, 1_000, 0, []),
        number=qtd_execucoes
    )
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: desloca_type_ignores(ignores, 1_000, 0, []))
    _ncal, _tcal = _bench.autorange()      # calibra: lote com _tcal >= 0.2s
    if _tcal >= _T:
        _k, _e = _ncal, _tcal              # a calibracao ja cobriu a duracao
    else:
        _alvo = max(1, round(_T / (_tcal / _ncal)))
        _e = _bench.timeit(number=_alvo)   # roda ~T segundos
        _k = _alvo
    _execucoes = _k * (_T / _e)            # normaliza para exatamente T
    print(f"execucoes em {_T}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
