import ast

# Funcao recursiva que manipula um no ast.Interactive.
# Analoga ao constant folding do manipula_no_expression.py, mas a raiz aqui
# e um Interactive (mode="single"), cujo body e uma LISTA de statements.
# Percorre recursivamente cada statement e dobra as sub-expressoes constantes,
# devolvendo um NOVO no ast.Interactive ja simplificado.
#
# OBS: esta e a versao COM list comprehension. Ela NAO e compativel com o
# transformador recpython3 (a variavel de laco da comprehension tem escopo
# proprio e e perdida na conversao). A versao compativel, com laco for
# explicito, esta em recursive_functions/newfunc/manipula_no_interactive.py


def dobra_interactive(no):
    """Recebe e devolve um no, simplificando recursivamente constantes.

    - ast.Interactive: manipula o no raiz, dobrando recursivamente cada stmt.
    - ast.Expr:        statement-expressao; dobra recursivamente seu value.
    - ast.BinOp:       dobra os dois lados; se ambos viram constantes, avalia.
    - ast.UnaryOp:     dobra o operando; se virou constante, avalia.
    - ast.Constant:    caso base, devolve a si mesmo.
    """
    # No Interactive: caso da raiz -> recursao sobre cada statement do body
    if isinstance(no, ast.Interactive):
        return ast.Interactive(body=[dobra_interactive(s) for s in no.body])

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


# Demonstracao: parse em mode="single" produz a raiz ast.Interactive
codigo = "2 * (3 + 4) - -5"
arvore = ast.parse(codigo, mode="single")
print("Tipo da raiz:", type(arvore).__name__)
print("Antes :", ast.unparse(arvore))

simplificada = dobra_interactive(arvore)
ast.fix_missing_locations(simplificada)
print("Depois:", ast.unparse(simplificada))

# A raiz simplificada continua sendo um no Interactive
print("Raiz ainda e Interactive?", isinstance(simplificada, ast.Interactive))
# Compilado em "single", o resultado e exibido como no REPL
print("Execucao em modo single:", end=" ")
exec(compile(simplificada, "<ast>", "single"))
