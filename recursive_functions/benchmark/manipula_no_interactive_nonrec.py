import ast
import os
import sys
import timeit

sys.setrecursionlimit(10000)

def dobra_interactive(no):
    _P = []
    _P.append((no, None, None, None, None, None, None, None, None, None, None, None, None, 0))
    while len(_P) > 0:
        no, novo_body, s, esq, dir, valor, operando, _for1, _r1, _r2, _r3, _r4, _r5, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s == 0:
            'Recebe e devolve um no, simplificando recursivamente constantes.\n\n    - ast.Interactive: manipula o no raiz, dobrando recursivamente cada stmt.\n    - ast.Expr:        statement-expressao; dobra recursivamente seu value.\n    - ast.BinOp:       dobra os dois lados; se ambos viram constantes, avalia.\n    - ast.UnaryOp:     dobra o operando; se virou constante, avalia.\n    - ast.Constant:    caso base, devolve a si mesmo.\n    '
        if _s in [1] or (_s == 0 and isinstance(no, ast.Interactive)):
            if _s == 0:
                novo_body = []
            if _s == 0:
                _for1 = iter(no.body)
            while _s in [1] or (_s == 0 and True):
                try:
                    if _s == 0:
                        s = next(_for1)
                    if _s == 0:
                        _P.append((no, novo_body, s, esq, dir, valor, operando, _for1, _r1, _r2, _r3, _r4, _r5, 1))
                        _P.append((s, None, None, None, None, None, None, None, None, None, None, None, None, 0))
                        _s = -1
                    elif _s == 1:
                        _r1 = _r
                        _s = 0
                    if _s == 0:
                        novo_body.append(_r1)
                except StopIteration:
                    break
            if _s == 0:
                _r = ast.Interactive(body=novo_body)
                _s = -1
        if _s in [2] or (_s == 0 and isinstance(no, ast.Expr)):
            if _s == 0:
                _P.append((no, novo_body, s, esq, dir, valor, operando, _for1, _r1, _r2, _r3, _r4, _r5, 2))
                _P.append((no.value, None, None, None, None, None, None, None, None, None, None, None, None, 0))
                _s = -1
            elif _s == 2:
                _r2 = _r
                _s = 0
            if _s == 0:
                _r = ast.Expr(value=_r2)
                _s = -1
        if _s in [] or (_s == 0 and isinstance(no, ast.Constant)):
            if _s == 0:
                _r = no
                _s = -1
        if _s in [3, 4] or (_s == 0 and isinstance(no, ast.BinOp)):
            if _s == 0:
                _P.append((no, novo_body, s, esq, dir, valor, operando, _for1, _r1, _r2, _r3, _r4, _r5, 3))
                _P.append((no.left, None, None, None, None, None, None, None, None, None, None, None, None, 0))
                _s = -1
            elif _s == 3:
                _r3 = _r
                _s = 0
            if _s == 0:
                esq = _r3
            if _s == 0:
                _P.append((no, novo_body, s, esq, dir, valor, operando, _for1, _r1, _r2, _r3, _r4, _r5, 4))
                _P.append((no.right, None, None, None, None, None, None, None, None, None, None, None, None, 0))
                _s = -1
            elif _s == 4:
                _r4 = _r
                _s = 0
            if _s == 0:
                dir = _r4
            if _s in [] or (_s == 0 and (isinstance(esq, ast.Constant) and isinstance(dir, ast.Constant))):
                if _s == 0:
                    valor = _aplica_binop(no.op, esq.value, dir.value)
                if _s == 0:
                    _r = ast.Constant(value=valor)
                    _s = -1
            if _s == 0:
                _r = ast.BinOp(left=esq, op=no.op, right=dir)
                _s = -1
        if _s in [5] or (_s == 0 and isinstance(no, ast.UnaryOp)):
            if _s == 0:
                _P.append((no, novo_body, s, esq, dir, valor, operando, _for1, _r1, _r2, _r3, _r4, _r5, 5))
                _P.append((no.operand, None, None, None, None, None, None, None, None, None, None, None, None, 0))
                _s = -1
            elif _s == 5:
                _r5 = _r
                _s = 0
            if _s == 0:
                operando = _r5
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
codigo = '1' + ' + 1' * 1000
arvore = ast.parse(codigo, mode='single')
qtd_execucoes = 1000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(lambda: dobra_interactive(arvore), number=qtd_execucoes)
    print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')
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
