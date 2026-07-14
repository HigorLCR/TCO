import sys
import timeit
import ast
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


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: desloca_type_ignores(ignores, 1000, 0, []))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
