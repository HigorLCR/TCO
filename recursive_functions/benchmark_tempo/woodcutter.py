def woodcutter(t, wood, lower, upper):
    middle_h = (lower + upper) // 2
    wood_collected = sum(max(0, tree - middle_h) for tree in t)

    if wood_collected == wood or lower == upper:
        return middle_h
    elif lower == upper - 1:
        if sum(max(0, tree - upper) for tree in t) >= wood:
            return upper
        else:
            return lower
    elif wood_collected > wood:
        return woodcutter(t, wood, middle_h, upper)
 


import timeit

arvores = list(range(1, 100001))
madeira = 1250025000
altura_minima = 0
altura_maxima = max(arvores)


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: woodcutter(arvores, madeira, altura_minima, altura_maxima))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
