"""
Mede a cobertura de nos AST de Python em um diretorio de arquivos .py.

Uso:
    python scripts/ast_coverage.py [diretorio]

Padrao: recursive_functions/benchmark
Exclui: arquivos com sufixo _nonrec.py e prefixo output_
"""

import ast
import sys
from pathlib import Path

# 107 nos recomendados, organizados por categoria
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


def is_source_file(path: Path) -> bool:
    name = path.name
    return (
        name.endswith(".py")
        and not name.endswith("_nonrec.py")
        and not name.startswith("output_")
        and name != "ast_coverage.py"
    )


def collect_nodes(path: Path) -> set[str]:
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except SyntaxError as e:
        print(f"  [ERRO] {path.name}: {e}")
        return set()
    return {type(node).__name__ for node in ast.walk(tree)}


def run(directory: Path) -> None:
    files = sorted(f for f in directory.iterdir() if f.is_file() and is_source_file(f))

    if not files:
        print(f"Nenhum arquivo fonte encontrado em: {directory}")
        return

    covered_per_file: dict[str, set[str]] = {}
    all_covered: set[str] = set()

    for f in files:
        nodes = collect_nodes(f) & ALL_TARGET
        covered_per_file[f.name] = nodes
        all_covered |= nodes

    total = len(ALL_TARGET)
    covered = len(all_covered)
    missing = ALL_TARGET - all_covered

    SEP = "=" * 60
    BAR_WIDTH = 30

    print(f"\n{SEP}")
    print(f"  Diretorio : {directory}")
    print(f"  Arquivos  : {len(files)}")
    print(f"  Cobertura : {covered}/{total} nos  ({covered/total*100:.1f}%)")

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

    print(f"\n{SEP}")
    print("  Cobertura por arquivo")
    print(f"{SEP}\n")
    for fname, nodes in covered_per_file.items():
        pct = len(nodes) / total * 100
        print(f"  {fname:<45} {len(nodes):>3}/{total}  ({pct:5.1f}%)")
    print(f"\n{SEP}")


if __name__ == "__main__":
    base = Path(__file__).parent.parent  # sobe de scripts/ para raiz do projeto

    if len(sys.argv) > 1:
        target_dir = Path(sys.argv[1])
        if not target_dir.is_absolute():
            target_dir = base / target_dir
    else:
        target_dir = base / "recursive_functions" / "benchmark"

    if not target_dir.is_dir():
        print(f"Diretorio nao encontrado: {target_dir}")
        sys.exit(1)

    run(target_dir)
