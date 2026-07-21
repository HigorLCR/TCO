import ast
import sys

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

# --- benchmark ---
def chamada():
    return desloca_type_ignores(ignores, 1_000, 0, [])
