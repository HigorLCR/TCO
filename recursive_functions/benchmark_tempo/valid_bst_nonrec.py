import io
import timeit

class TreeNode:

    def __init__(self, val, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right

class _Empty:
    pass
type NodeOrNone = TreeNode | None

def is_valid_bst(node, lo=None, hi=None):
    _P = []
    _P.append((node, lo, hi, None, None, 0))
    while len(_P) > 0:
        node, lo, hi, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and node is None):
            if _s == 0:
                _r = True
                _s = -1
        if _s in [] or (_s == 0 and (lo is not None and node.val <= lo)):
            if _s == 0:
                _r = False
                _s = -1
        if _s in [] or (_s == 0 and (hi is not None and node.val >= hi)):
            if _s == 0:
                _r = False
                _s = -1
        if _s == 0:
            _P.append((node, lo, hi, _r1, _r2, 1))
            _P.append((node.left, lo, node.val, None, None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            _P.append((node, lo, hi, _r1, _r2, 2))
            _P.append((node.right, node.val, hi, None, None, 0))
            _s = -1
        elif _s == 2:
            _r2 = _r
            _s = 0
        if _s == 0:
            _r = _r1 and _r2
            _s = -1
    return _r

def build_bst(values):
    _P = []
    _P.append((values, None, None, None, None, 0))
    while len(_P) > 0:
        values, mid, node, _r1, _r2, _s = _P.pop()
        if _s == 0:
            _r = None
        if _s in [] or (_s == 0 and (not values)):
            if _s == 0:
                _r = None
                _s = -1
        if _s == 0:
            mid = len(values) // 2
        if _s == 0:
            node = TreeNode(values[mid])
        if _s == 0:
            _P.append((values, mid, node, _r1, _r2, 1))
            _P.append((values[:mid], None, None, None, None, 0))
            _s = -1
        elif _s == 1:
            _r1 = _r
            _s = 0
        if _s == 0:
            node.left = _r1
        if _s == 0:
            _P.append((values, mid, node, _r1, _r2, 2))
            _P.append((values[mid + 1:], None, None, None, None, 0))
            _s = -1
        elif _s == 2:
            _r2 = _r
            _s = 0
        if _s == 0:
            node.right = _r2
        if _s == 0:
            _r = node
            _s = -1
    return _r
n = 1000
root = build_bst(list(range(n)))
with io.StringIO() as buf:
    buf.write(f'root.val = {root.val}')


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: is_valid_bst(root))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
