import sys
import timeit
import ast
sys.setrecursionlimit(10000)

def mapeia_tipos(no, mapa):
    _P = []
    _P.append((no, mapa, None, None, None, None, None, None, None, None, None, None, None, 0))
    while len(_P) > 0:
        no, mapa, novos_argtypes, a, novos_elts, e, _for1, _for2, _r1, _r2, _r3, _r4, _r5, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s == 0:
            'Recebe e devolve um no, renomeando recursivamente nomes de tipo.\n\n    - ast.FunctionType: manipula o no raiz, recursando em argtypes e returns.\n    - ast.Subscript:    tipo generico (list[int]); recursa no value e no slice.\n    - ast.Tuple:        varios tipos (dict[str, int]); recursa em cada elemento.\n    - ast.Name:         caso base/folha; aplica o mapa de renomeacao.\n    '
        if _s in [1, 2] or (_s == 0 and isinstance(no, ast.FunctionType)):
            if _s == 0:
                novos_argtypes = []
            if _s == 0:
                _for1 = iter(no.argtypes)
            while _s in [1] or (_s == 0 and True):
                try:
                    if _s == 0:
                        a = next(_for1)
                    if _s == 0:
                        _P.append((no, mapa, novos_argtypes, a, novos_elts, e, _for1, _for2, _r1, _r2, _r3, _r4, _r5, 1))
                        _P.append((a, mapa, None, None, None, None, None, None, None, None, None, None, None, 0))
                        _s = -1
                    elif _s == 1:
                        _r1 = _r
                        _s = 0
                    if _s == 0:
                        novos_argtypes.append(_r1)
                except StopIteration:
                    break
            if _s == 0:
                _P.append((no, mapa, novos_argtypes, a, novos_elts, e, _for1, _for2, _r1, _r2, _r3, _r4, _r5, 2))
                _P.append((no.returns, mapa, None, None, None, None, None, None, None, None, None, None, None, 0))
                _s = -1
            elif _s == 2:
                _r2 = _r
                _s = 0
            if _s == 0:
                _r = ast.FunctionType(argtypes=novos_argtypes, returns=_r2)
                _s = -1
        if _s in [3, 4] or (_s == 0 and isinstance(no, ast.Subscript)):
            if _s == 0:
                _P.append((no, mapa, novos_argtypes, a, novos_elts, e, _for1, _for2, _r1, _r2, _r3, _r4, _r5, 3))
                _P.append((no.value, mapa, None, None, None, None, None, None, None, None, None, None, None, 0))
                _s = -1
            elif _s == 3:
                _r3 = _r
                _s = 0
            if _s == 0:
                _P.append((no, mapa, novos_argtypes, a, novos_elts, e, _for1, _for2, _r1, _r2, _r3, _r4, _r5, 4))
                _P.append((no.slice, mapa, None, None, None, None, None, None, None, None, None, None, None, 0))
                _s = -1
            elif _s == 4:
                _r4 = _r
                _s = 0
            if _s == 0:
                _r = ast.Subscript(value=_r3, slice=_r4, ctx=ast.Load())
                _s = -1
        if _s in [5] or (_s == 0 and isinstance(no, ast.Tuple)):
            if _s == 0:
                novos_elts = []
            if _s == 0:
                _for2 = iter(no.elts)
            while _s in [5] or (_s == 0 and True):
                try:
                    if _s == 0:
                        e = next(_for2)
                    if _s == 0:
                        _P.append((no, mapa, novos_argtypes, a, novos_elts, e, _for1, _for2, _r1, _r2, _r3, _r4, _r5, 5))
                        _P.append((e, mapa, None, None, None, None, None, None, None, None, None, None, None, 0))
                        _s = -1
                    elif _s == 5:
                        _r5 = _r
                        _s = 0
                    if _s == 0:
                        novos_elts.append(_r5)
                except StopIteration:
                    break
            if _s == 0:
                _r = ast.Tuple(elts=novos_elts, ctx=ast.Load())
                _s = -1
        if _s in [] or (_s == 0 and isinstance(no, ast.Name)):
            if _s == 0:
                _r = ast.Name(id=mapa.get(no.id, no.id), ctx=ast.Load())
                _s = -1
        if _s == 0:
            _r = no
            _s = -1
    return _r
profundidade = 1000
arvore_tipo = ast.Name(id='int', ctx=ast.Load())
for _ in range(profundidade):
    arvore_tipo = ast.Subscript(value=ast.Name(id='list', ctx=ast.Load()), slice=arvore_tipo, ctx=ast.Load())
arvore = ast.FunctionType(argtypes=[arvore_tipo], returns=ast.Name(id='bool', ctx=ast.Load()))
renomeacao = {'int': 'Inteiro', 'bool': 'Booleano'}
qtd_execucoes = 1000
tempo = timeit.timeit(lambda: mapeia_tipos(arvore, renomeacao), number=qtd_execucoes)
print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')