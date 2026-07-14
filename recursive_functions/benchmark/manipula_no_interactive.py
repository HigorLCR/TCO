import ast
import os
import sys
import timeit

sys.setrecursionlimit(10_000)

# Funcao recursiva que manipula um no ast.Interactive.
# Analoga ao constant folding do manipula_no_expression.py, mas a raiz aqui
# e um Interactive (mode="single"), cujo body e uma LISTA de statements.
# Percorre recursivamente cada statement e dobra as sub-expressoes constantes,
# devolvendo um NOVO no ast.Interactive ja simplificado.


def dobra_interactive(no):
    """Recebe e devolve um no, simplificando recursivamente constantes.

    - ast.Interactive: manipula o no raiz, dobrando recursivamente cada stmt.
    - ast.Expr:        statement-expressao; dobra recursivamente seu value.
    - ast.BinOp:       dobra os dois lados; se ambos viram constantes, avalia.
    - ast.UnaryOp:     dobra o operando; se virou constante, avalia.
    - ast.Constant:    caso base, devolve a si mesmo.
    """
    # No Interactive: caso da raiz -> recursao sobre cada statement do body.
    # Laco for explicito (sem comprehension) para ser compativel com o recpython.
    if isinstance(no, ast.Interactive):
        novo_body = []
        for s in no.body:
            novo_body.append(dobra_interactive(s))
        return ast.Interactive(body=novo_body)

    # Statement-expressao: dobra recursivamente a expressao que ele carrega
    if isinstance(no, ast.Expr):
        return ast.Expr(value=dobra_interactive(no.value))

    # Caso base: constante nao se simplifica mais
    if isinstance(no, ast.Constant):
        return no

    # Operacao binaria: dobra recursivamente os dois operandos
    if isinstance(no, ast.BinOp):
        esq = dobra_interactive(no.left)
        dir = dobra_interactive(no.right)
        if isinstance(esq, ast.Constant) and isinstance(dir, ast.Constant):
            valor = _aplica_binop(no.op, esq.value, dir.value)
            return ast.Constant(value=valor)
        return ast.BinOp(left=esq, op=no.op, right=dir)

    # Operacao unaria: dobra recursivamente o operando
    if isinstance(no, ast.UnaryOp):
        operando = dobra_interactive(no.operand)
        if isinstance(operando, ast.Constant):
            valor = _aplica_unaryop(no.op, operando.value)
            return ast.Constant(value=valor)
        return ast.UnaryOp(op=no.op, operand=operando)

    # Qualquer outro no fica inalterado
    return no


def _aplica_binop(op, a, b):
    if isinstance(op, ast.Add):
        return a + b
    if isinstance(op, ast.Sub):
        return a - b
    if isinstance(op, ast.Mult):
        return a * b
    if isinstance(op, ast.Div):
        return a / b
    raise ValueError(f"operador binario nao suportado: {type(op).__name__}")


def _aplica_unaryop(op, a):
    if isinstance(op, ast.USub):
        return -a
    if isinstance(op, ast.UAdd):
        return +a
    raise ValueError(f"operador unario nao suportado: {type(op).__name__}")


# Entrada do benchmark: expressao aritmetica profunda parseada como Interactive
codigo = "1" + " + 1" * 1_000
arvore = ast.parse(codigo, mode="single")

qtd_execucoes = 1_000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(
        lambda: dobra_interactive(arvore),
        number=qtd_execucoes
    )
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: dobra_interactive(arvore))
    _ncal, _tcal = _bench.autorange()      # calibra: lote com _tcal >= 0.2s
    if _tcal >= _T:
        _k, _e = _ncal, _tcal              # a calibracao ja cobriu a duracao
    else:
        _alvo = max(1, round(_T / (_tcal / _ncal)))
        _e = _bench.timeit(number=_alvo)   # roda ~T segundos
        _k = _alvo
    _execucoes = _k * (_T / _e)            # normaliza para exatamente T
    print(f"execucoes em {_T}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
