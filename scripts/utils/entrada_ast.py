"""
Extracao da ENTRADA de um arquivo medido, por AST — nada e executado.

De `def chamada(): return f(N, 10000)` sai a string `"[1 for i in range(10000)], 10000"`:
os argumentos reais da chamada, com as variaveis de modulo ja resolvidas.

Usado pelo benchmark.py (fase de verificacao, para conferir que as versoes de
uma funcao recebem a mesma entrada) e pelo planilha_tempos.py (linha
'Parametros' da planilha). Vive em utils/ para os dois nao dependerem um do
outro.
"""

import ast
import re
from pathlib import Path


def _assignments(tree):
    """Atribuicoes no nivel raiz do modulo: {nome: no do valor}."""
    amap = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    amap[t.id] = node.value
    return amap


def _substitute(node, amap, depth=0):
    """Troca cada Name pelo valor atribuido a ele (recursivo, profundidade <= 4)."""
    if depth > 4:
        return node

    class R(ast.NodeTransformer):
        def visit_Name(self, n):
            if n.id in amap:
                return _substitute(
                    ast.parse(ast.unparse(amap[n.id]), mode="eval").body, amap, depth + 1)
            return n

    return R().visit(node)


def _achar_chamada(tree):
    """Call dentro de `def chamada(): return f(...)` no nivel de modulo."""
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == "chamada":
            for st in ast.walk(node):
                if isinstance(st, ast.Return) and isinstance(st.value, ast.Call):
                    return st.value
    return None


def _abreviar_numeros(texto: str) -> str:
    """Inteiros gigantes viram '353410...177320(207dig)' para caber no relatorio."""
    def repl(m):
        s = m.group()
        return f"{s[:6]}...{s[-6:]}({len(s)}dig)"
    return re.sub(r"\d{16,}", repl, texto)


def entrada_de(path: Path) -> str:
    """Args reais da chamada em def chamada(), resolvidos e formatados 'p1, p2, ...'."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, OSError):
        return "-"
    #coleta todas as atribuições no nivel raiz do script
    amap = _assignments(tree)
    #coleta a chamada medida em def chamada() e extrai seus argumentos, substituindo nomes por valores
    call = _achar_chamada(tree)
    if call is None:
        return "-"
    partes = []
    for a in call.args:
        partes.append(_abreviar_numeros(ast.unparse(_substitute(a, amap))))
    for kw in call.keywords:
        partes.append(f"{kw.arg}={_abreviar_numeros(ast.unparse(_substitute(kw.value, amap)))}")
    return ", ".join(partes) if partes else "-"
