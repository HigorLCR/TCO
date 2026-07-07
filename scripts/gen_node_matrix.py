"""
Regenera node_matrix.txt: matriz de cobertura de nos AST por arquivo-fonte.

Linhas  = tipos de no AST (uniao dos presentes), ordenadas.
Colunas = arquivos .py de recursive_functions/benchmark
          (exclui *_nonrec.py e output_*).
Celula  = 'X' se o no aparece naquele arquivo, '.' caso contrario.

Cobertura demonstrativa: arquivos no padrao 'manipula_no_<no>.py' cobrem nos que
NUNCA aparecem num parse estatico (mod: Interactive/Expression/FunctionType; e
TypeIgnore). Como esses nos so existem em runtime (construidos/parseados em modo
especial), marcamos o no-alvo de cada manipula_no_* como coberto, deduzindo-o
pelo sufixo do nome (ex.: manipula_no_typeignore.py -> TypeIgnore).

Formato preservado do arquivo original:
    UTF-16-LE com BOM, separador '|', quebras CRLF, 1a celula do cabecalho 'NO'.

Uso:
    python scripts/gen_node_matrix.py
"""

import ast
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
BENCH = BASE / "recursive_functions" / "benchmark"
OUT = BASE / "node_matrix.txt"

HEADER0 = "NO"
SEP = "|"
EOL = "\r\n"

PREFIXO_MANIPULA = "manipula_no_"

# nome do no AST indexado pela versao minuscula (ex.: "typeignore" -> "TypeIgnore")
NO_POR_MINUSCULO = {
    n.lower(): n
    for n in dir(ast)
    if isinstance(getattr(ast, n), type) and issubclass(getattr(ast, n), ast.AST)
}


def no_demonstrativo(nome_arquivo: str) -> str | None:
    """Para 'manipula_no_<no>.py', devolve o no AST alvo (cobertura demonstrativa).

    Deduz pelo sufixo: o no cujo nome em minusculas casa com o sufixo.
    Ex.: 'manipula_no_functiontype.py' -> 'FunctionType'.
    """
    stem = nome_arquivo[:-3] if nome_arquivo.endswith(".py") else nome_arquivo
    if not stem.startswith(PREFIXO_MANIPULA):
        return None
    return NO_POR_MINUSCULO.get(stem[len(PREFIXO_MANIPULA):])


def is_source(p: Path) -> bool:
    n = p.name
    return (
        p.suffix == ".py"
        and not n.endswith("_nonrec.py")
        and not n.startswith("output_")
    )


def nodes_of(p: Path) -> set[str]:
    try:
        tree = ast.parse(p.read_text(encoding="utf-8"))
    except SyntaxError as e:
        print(f"  [ERRO] {p.name}: {e}")
        return set()
    return {type(n).__name__ for n in ast.walk(tree)}


def main() -> None:
    if not BENCH.is_dir():
        print(f"Diretorio nao encontrado: {BENCH}")
        sys.exit(1)

    files = sorted(p for p in BENCH.iterdir() if p.is_file() and is_source(p))
    if not files:
        print(f"Nenhum arquivo-fonte em: {BENCH}")
        sys.exit(1)

    cobertura = {p.name: nodes_of(p) for p in files}

    # cobertura demonstrativa dos manipula_no_*: injeta o no-alvo (runtime).
    demonstrativos = {}
    for nome in cobertura:
        if nome.startswith(PREFIXO_MANIPULA):
            alvo = no_demonstrativo(nome)
            if alvo:
                cobertura[nome].add(alvo)
                demonstrativos[nome] = alvo
            else:
                print(f"  [AVISO] {nome}: sufixo nao casa com nenhum no AST")

    todos_nos = sorted(set().union(*cobertura.values()))

    nomes = [p.name for p in files]
    linhas = [HEADER0 + SEP + SEP.join(nomes)]
    for no in todos_nos:
        celulas = ["X" if no in cobertura[nome] else "." for nome in nomes]
        linhas.append(no + SEP + SEP.join(celulas))

    conteudo = "﻿" + EOL.join(linhas) + EOL
    with open(OUT, "w", encoding="utf-16-le", newline="") as f:
        f.write(conteudo)

    # resumo
    print(f"Arquivos (colunas) : {len(files)}")
    print(f"Nos distintos (linhas): {len(todos_nos)}")
    if demonstrativos:
        print("Cobertura demonstrativa (manipula_no_*):")
        for nome, alvo in demonstrativos.items():
            print(f"  {nome:<34} -> {alvo}")
    print(f"Salvo: {OUT}")
    print("\nCobertura por arquivo (nos distintos):")
    for nome in nomes:
        print(f"  {nome:<38} {len(cobertura[nome]):>3}")


if __name__ == "__main__":
    main()
