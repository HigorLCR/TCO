"""
Cobertura de nos AST dos fontes do benchmark: relatorio no terminal e,
opcionalmente, a matriz node_matrix.txt consumida pelo planilha_cobertura.py.

Um unico parse (ast.parse + ast.walk por arquivo) alimenta as duas saidas:

  RELATORIO (sempre): cobertura dos 110 nos-alvo (TARGET_NODES) -- global,
    por categoria da gramatica ASDL, nos faltantes e acumulada por arquivo.

  MATRIZ (--matriz): grava arquivos/txt/node_matrix.txt -- linhas = uniao dos
    nos presentes (ordenada), colunas = arquivos, celula 'X'/'.'. Formato
    preservado do arquivo original: UTF-16-LE com BOM, separador '|', CRLF,
    1a celula do cabecalho 'NO'.

Cobertura demonstrativa (aplicada as DUAS saidas): arquivos no padrao
'manipula_no_<no>.py' cobrem nos que NUNCA aparecem num parse estatico
(Interactive/Expression/FunctionType, raizes de outros modos de parse; e
TypeIgnore, que exige type_comments=True). Como esses nos so existem em
runtime, o no-alvo de cada manipula_no_* e deduzido pelo sufixo do nome
(ex.: manipula_no_typeignore.py -> TypeIgnore) e marcado como coberto.

Uso:
    python scripts/cobertura.py [diretorio] [--matriz]

Padrao: recursive_functions/benchmark
Exclui: arquivos com sufixo _nonrec.py e prefixo output_
"""

import ast
import sys
from pathlib import Path

BASE = Path(__file__).parent.parent
BENCH = BASE / "recursive_functions" / "benchmark"
OUT = BASE / "arquivos" / "txt" / "node_matrix.txt"

# 110 nos recomendados, organizados por categoria
TARGET_NODES: dict[str, list[str]] = {
    "mod": [
        "Module", "Interactive", "Expression", "FunctionType",
    ],
    "stmt": [
        "FunctionDef", "AsyncFunctionDef", "ClassDef",
        "Return", "Delete", "Assign", "TypeAlias", "AugAssign", "AnnAssign",
        "For", "AsyncFor", "While", "If", "With", "AsyncWith", "Match",
        "Raise", "Try", "TryStar", "Assert",
        "Import", "ImportFrom",
        "Global", "Nonlocal",
        "Expr", "Pass", "Break", "Continue",
    ],
    "expr": [
        "BoolOp", "NamedExpr", "BinOp", "UnaryOp", "Lambda", "IfExp",
        "Dict", "Set", "ListComp", "SetComp", "DictComp", "GeneratorExp",
        "Await", "Yield", "YieldFrom",
        "Compare", "Call",
        "FormattedValue", "JoinedStr",
        "Constant", "Attribute", "Subscript", "Starred", "Name",
        "List", "Tuple", "Slice",
    ],
    "expr_context": [
        "Load", "Store", "Del",
    ],
    "operator": [
        "Add", "Sub", "Mult", "MatMult", "Div", "Mod", "Pow",
        "LShift", "RShift", "BitOr", "BitXor", "BitAnd", "FloorDiv",
    ],
    "unaryop": [
        "Invert", "Not", "UAdd", "USub",
    ],
    "boolop": [
        "And", "Or",
    ],
    "cmpop": [
        "Eq", "NotEq", "Lt", "LtE", "Gt", "GtE",
        "Is", "IsNot", "In", "NotIn",
    ],
    "pattern": [
        "MatchValue", "MatchSingleton", "MatchSequence", "MatchStar",
        "MatchMapping", "MatchClass", "MatchAs", "MatchOr",
    ],
    "type_param": [
        "TypeVar", "ParamSpec", "TypeVarTuple",
    ],
    "auxiliar": [
        "arguments", "arg", "keyword", "alias",
        "withitem", "match_case", "ExceptHandler", "comprehension",
    ],
}

ALL_TARGET = {node for nodes in TARGET_NODES.values() for node in nodes}

HEADER0 = "NO"
COL_SEP = "|"
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


def coletar(directory: Path) -> tuple[dict[str, set[str]], dict[str, str]]:
    """Parse unico de todos os fontes; devolve ({arquivo: nos}, {arquivo: no demonstrativo}).

    Ja injeta a cobertura demonstrativa dos manipula_no_* -- vale para o
    relatorio E para a matriz.
    """
    files = sorted(p for p in directory.iterdir() if p.is_file() and is_source(p))
    if not files:
        print(f"Nenhum arquivo-fonte em: {directory}")
        sys.exit(1)

    cobertura = {p.name: nodes_of(p) for p in files}

    demonstrativos = {}
    for nome in cobertura:
        if nome.startswith(PREFIXO_MANIPULA):
            alvo = no_demonstrativo(nome)
            if alvo:
                cobertura[nome].add(alvo)
                demonstrativos[nome] = alvo
            else:
                print(f"  [AVISO] {nome}: sufixo nao casa com nenhum no AST")

    return cobertura, demonstrativos


# ==================== relatorio no terminal ====================

def relatorio(directory: Path, cobertura: dict[str, set[str]],
              demonstrativos: dict[str, str]) -> None:
    all_covered = set().union(*cobertura.values()) & ALL_TARGET

    total = len(ALL_TARGET)
    covered = len(all_covered)
    missing = ALL_TARGET - all_covered

    SEP = "=" * 60
    BAR_WIDTH = 30

    print(f"\n{SEP}")
    print(f"  Diretorio : {directory}")
    print(f"  Arquivos  : {len(cobertura)}")
    print(f"  Cobertura : {covered}/{total} nos  ({covered/total*100:.1f}%)")

    if demonstrativos:
        print(f"\n{SEP}")
        print("  Cobertura demonstrativa (manipula_no_*, nos de runtime)")
        print(f"{SEP}\n")
        for nome, alvo in demonstrativos.items():
            print(f"  {nome:<40} -> {alvo}")

    print(f"\n{SEP}")
    print("  Cobertura por categoria")
    print(f"{SEP}\n")
    for category, nodes in TARGET_NODES.items():
        cat_covered = {n for n in nodes if n in all_covered}
        cat_missing  = [n for n in nodes if n not in all_covered]
        pct = len(cat_covered) / len(nodes) * 100
        filled = round(pct / 100 * BAR_WIDTH)
        bar = "#" * filled + "." * (BAR_WIDTH - filled)
        print(f"  {category:<14} {bar}  {len(cat_covered):>2}/{len(nodes)}  ({pct:5.1f}%)")
        if cat_missing:
            print(f"               faltando: {', '.join(cat_missing)}\n")

    print(f"\n{SEP}")
    print(f"  Nos nao cobertos ({len(missing)})")
    print(f"{SEP}\n")
    for category, nodes in TARGET_NODES.items():
        uncovered = [n for n in nodes if n in missing]
        if uncovered:
            print(f"  [{category}] {', '.join(uncovered)}")

    # progressiva, na mesma ordem da planilha de cobertura: cada arquivo
    # mostra os nos-alvo NOVOS que trouxe e o acumulado ate ali
    print(f"\n{SEP}")
    print("  Cobertura por arquivo (acumulada)")
    print(f"{SEP}\n")
    acumulado: set[str] = set()
    for fname, nodes in cobertura.items():
        novos = (nodes & ALL_TARGET) - acumulado
        acumulado |= novos
        pct = len(acumulado) / total * 100
        print(f"  {fname:<45} +{len(novos):>2}  {len(acumulado):>3}/{total}  ({pct:5.1f}%)")
    print(f"\n{SEP}")


# ==================== matriz node_matrix.txt ====================

def gravar_matriz(cobertura: dict[str, set[str]]) -> None:
    """Grava a matriz nos x arquivos (uniao dos nos presentes, nao so os alvo)."""
    todos_nos = sorted(set().union(*cobertura.values()))
    nomes = list(cobertura)

    linhas = [HEADER0 + COL_SEP + COL_SEP.join(nomes)]
    for no in todos_nos:
        celulas = ["X" if no in cobertura[nome] else "." for nome in nomes]
        linhas.append(no + COL_SEP + COL_SEP.join(celulas))

    conteudo = "﻿" + EOL.join(linhas) + EOL
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(OUT, "w", encoding="utf-16-le", newline="") as f:
        f.write(conteudo)

    print(f"\n  Matriz: {len(todos_nos)} nos x {len(nomes)} arquivos  ->  {OUT}")


def main() -> None:
    directory = BENCH
    matriz = False
    for arg in sys.argv[1:]:
        if arg == "--matriz":
            matriz = True
        else:
            directory = Path(arg)
            if not directory.is_absolute():
                directory = BASE / directory

    if not directory.is_dir():
        print(f"Diretorio nao encontrado: {directory}")
        sys.exit(1)

    cobertura, demonstrativos = coletar(directory)
    relatorio(directory, cobertura, demonstrativos)
    if matriz:
        gravar_matriz(cobertura)


if __name__ == "__main__":
    main()
