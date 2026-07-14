import ast

def dobra_expressao(no):
    _P = []
    _P.append((no, None, None, None, None, None, None, None, None, 0))
    while len(_P) > 0:
        no, esq, dir, valor, operando, _r1, _r2, _r3, _r4, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s == 0:
            'Recebe e devolve um no, simplificando recursivamente constantes.\n\n    - ast.Expression: manipula o no raiz, dobrando recursivamente seu body.\n    - ast.BinOp:      dobra os dois lados; se ambos viram constantes, avalia.\n    - ast.UnaryOp:    dobra o operando; se virou constante, avalia.\n    - ast.Constant:   caso base, devolve a si mesmo.\n    '
        if _s in [1] or (_s == 0 and isinstance(no, ast.Expression)):
            if _s == 0:
                _P.append((no, esq, dir, valor, operando, _r1, _r2, _r3, _r4, 1))
                _P.append((no.body, None, None, None, None, None, None, None, None, 0))
                _s = -1
            elif _s == 1:
                _r1 = _r
                _s = 0
            if _s == 0:
                _r = ast.Expression(body=_r1)
                _s = -1
        if _s in [] or (_s == 0 and isinstance(no, ast.Constant)):
            if _s == 0:
                _r = no
                _s = -1
        if _s in [2, 3] or (_s == 0 and isinstance(no, ast.BinOp)):
            if _s == 0:
                _P.append((no, esq, dir, valor, operando, _r1, _r2, _r3, _r4, 2))
                _P.append((no.left, None, None, None, None, None, None, None, None, 0))
                _s = -1
            elif _s == 2:
                _r2 = _r
                _s = 0
            if _s == 0:
                esq = _r2
            if _s == 0:
                _P.append((no, esq, dir, valor, operando, _r1, _r2, _r3, _r4, 3))
                _P.append((no.right, None, None, None, None, None, None, None, None, 0))
                _s = -1
            elif _s == 3:
                _r3 = _r
                _s = 0
            if _s == 0:
                dir = _r3
            if _s in [] or (_s == 0 and (isinstance(esq, ast.Constant) and isinstance(dir, ast.Constant))):
                if _s == 0:
                    valor = _aplica_binop(no.op, esq.value, dir.value)
                if _s == 0:
                    _r = ast.Constant(value=valor)
                    _s = -1
            if _s == 0:
                _r = ast.BinOp(left=esq, op=no.op, right=dir)
                _s = -1
        if _s in [4] or (_s == 0 and isinstance(no, ast.UnaryOp)):
            if _s == 0:
                _P.append((no, esq, dir, valor, operando, _r1, _r2, _r3, _r4, 4))
                _P.append((no.operand, None, None, None, None, None, None, None, None, 0))
                _s = -1
            elif _s == 4:
                _r4 = _r
                _s = 0
            if _s == 0:
                operando = _r4
            if _s in [] or (_s == 0 and isinstance(operando, ast.Constant)):
                if _s == 0:
                    valor = _aplica_unaryop(no.op, operando.value)
                if _s == 0:
                    _r = ast.Constant(value=valor)
                    _s = -1
            if _s == 0:
                _r = ast.UnaryOp(op=no.op, operand=operando)
                _s = -1
        if _s == 0:
            _r = no
            _s = -1
    return _r

def _aplica_binop(op, a, b):
    if isinstance(op, ast.Add):
        return a + b
    if isinstance(op, ast.Sub):
        return a - b
    if isinstance(op, ast.Mult):
        return a * b
    if isinstance(op, ast.Div):
        return a / b
    raise ValueError(f'operador binario nao suportado: {type(op).__name__}')

def _aplica_unaryop(op, a):
    if isinstance(op, ast.USub):
        return -a
    if isinstance(op, ast.UAdd):
        return +a
    raise ValueError(f'operador unario nao suportado: {type(op).__name__}')
codigo = '2 * (3 + 4) - -5'
arvore = ast.parse(codigo, mode='eval')
print('Tipo da raiz:', type(arvore).__name__)
print('Antes :', ast.unparse(arvore))
simplificada = dobra_expressao(arvore)
ast.fix_missing_locations(simplificada)
print('Depois:', ast.unparse(simplificada))
print('Raiz ainda e Expression?', isinstance(simplificada, ast.Expression))
print('Resultado avaliado:', eval(compile(simplificada, '<ast>', 'eval')))
