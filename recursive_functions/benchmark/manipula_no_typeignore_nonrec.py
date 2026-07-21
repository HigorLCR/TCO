import ast
import sys

sys.setrecursionlimit(10000)

def desloca_type_ignores(ignores, offset, i, acc):
    _P = []
    _P.append((ignores, offset, i, acc, None, None, None, 0))
    while len(_P) > 0:
        ignores, offset, i, acc, no, novo, _r1, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s == 0:
            'Devolve uma nova lista de ast.TypeIgnore com lineno deslocado por offset.\n\n    Recursao de cauda sobre os indices (i, i+1, ...), compativel com o recpython.\n    - i >= len: caso base, devolve o acumulador.\n    - ast.TypeIgnore: manipula o no, somando offset ao lineno e mantendo a tag.\n    '
        if _s in [] or (_s == 0 and i >= len(ignores)):
            if _s == 0:
                _r = acc
                _s = -1
        if _s == 0:
            no = ignores[i]
        if _s == 0:
            novo = ast.TypeIgnore(lineno=no.lineno + offset, tag=no.tag)
        if _s == 0:
            acc.append(novo)
        if _s == 0:
            _P.append((ignores, offset, i, acc, no, novo, _r1, 1))
            _P.append((ignores, offset, i + 1, acc, None, None, None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            _r = _r1
            _s = -1
    return _r
quantidade = 1000
linhas = []
for j in range(quantidade):
    linhas.append(f'v{j} = {j}  # type: ignore')
codigo = '\n'.join(linhas)
ignores = ast.parse(codigo, type_comments=True).type_ignores

# --- benchmark ---
def chamada():
    return desloca_type_ignores(ignores, 1000, 0, [])
