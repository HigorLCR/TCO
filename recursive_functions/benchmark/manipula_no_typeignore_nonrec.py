import ast
import os
import sys
import timeit

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
qtd_execucoes = 1000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (T e piso: itera ate somar >= T s).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(lambda: desloca_type_ignores(ignores, 1000, 0, []), number=qtd_execucoes)
    print(f'tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo / qtd_execucoes * 1000:.4f}ms por chamada')
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: desloca_type_ignores(ignores, 1000, 0, []))
    _k, _e = 0, 0.0                        # iteracoes completas, tempo somado
    _lote = 1
    while _e < _T:                         # T e piso: so para ao alcanca-lo
        _e += _bench.timeit(number=_lote)
        _k += _lote
        if _e >= _T:
            break
        _est = int((_T - _e) / (_e / _k))  # estimativa do que falta pela taxa
        _lote = max(1, min(_est, _lote * 10))
    print(f"benchmark por tempo (piso {_T}s): {_k} iteracoes | {_e:.4f}s total | {_e/_k*1000:.4f}ms por chamada")
