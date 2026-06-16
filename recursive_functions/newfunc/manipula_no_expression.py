import ast

# Funcao recursiva que manipula um no ast.Expression.
# Ela faz "constant folding": percorre a arvore da expressao e avalia
# recursivamente as sub-expressoes constantes, devolvendo um NOVO no
# ast.Expression ja simplificado.


def dobra_expressao(no):
    """Recebe e devolve um no, simplificando recursivamente constantes.

    - ast.Expression: manipula o no raiz, dobrando recursivamente seu body.
    - ast.BinOp:      dobra os dois lados; se ambos viram constantes, avalia.
    - ast.UnaryOp:    dobra o operando; se virou constante, avalia.
    - ast.Constant:   caso base, devolve a si mesmo.
    """
    # No Expression: caso da raiz -> recursao sobre o body e remontagem do no
    if isinstance(no, ast.Expression):
        return ast.Expression(body=dobra_expressao(no.body))

    # Caso base: constante nao se simplifica mais
    if isinstance(no, ast.Constant):
        return no

    # Operacao binaria: dobra recursivamente os dois operandos
    if isinstance(no, ast.BinOp):
        esq = dobra_expressao(no.left)
        dir = dobra_expressao(no.right)
        if isinstance(esq, ast.Constant) and isinstance(dir, ast.Constant):
            valor = _aplica_binop(no.op, esq.value, dir.value)
            return ast.Constant(value=valor)
        return ast.BinOp(left=esq, op=no.op, right=dir)

    # Operacao unaria: dobra recursivamente o operando
    if isinstance(no, ast.UnaryOp):
        operando = dobra_expressao(no.operand)
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


# Demonstracao: parse em mode="eval" produz a raiz ast.Expression
codigo = "2 * (3 + 4) - -5"
arvore = ast.parse(codigo, mode="eval")
print("Tipo da raiz:", type(arvore).__name__)
print("Antes :", ast.unparse(arvore))

simplificada = dobra_expressao(arvore)
ast.fix_missing_locations(simplificada)
print("Depois:", ast.unparse(simplificada))

# A raiz simplificada continua sendo um no Expression
print("Raiz ainda e Expression?", isinstance(simplificada, ast.Expression))
print("Resultado avaliado:", eval(compile(simplificada, "<ast>", "eval")))
