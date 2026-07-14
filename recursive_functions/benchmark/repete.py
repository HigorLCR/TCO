import os
import sys
import timeit
from collections.abc import Callable

sys.setrecursionlimit(10_000)

# Cobre o no ParamSpec (PEP 695): o no vem do [**P] nos type_params, e P captura
# a assinatura de f via Callable[P, None].
# Para ser compativel com o recpython3, os argumentos de f sao passados como
# parametros NORMAIS (args: tuple, kwargs: dict) -> a chamada recursiva tem
# aridade FIXA. O unpacking *args/**kwargs ocorre so na chamada a f, que NAO e
# recursiva (logo o transformador nao mexe nela).


def repete[**P](f: Callable[P, None], n: int, args: tuple, kwargs: dict) -> None:
    if n <= 0:
        return None
    f(*args, **kwargs)
    repete(f, n - 1, args, kwargs)


def _noop(*args, **kwargs):
    pass


n = 1_000

qtd_execucoes = 1_000


# ===== driver condicional (classico x por tempo) =====
# Sem BENCH_DURACAO no ambiente: modo CLASSICO (qtd_execucoes iteracoes -> tempo).
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (T e piso: itera ate somar >= T s).
# A chamada medida e a MESMA nos dois modos.

if os.environ.get("BENCH_DURACAO") is None:
    tempo = timeit.timeit(
        lambda: repete(_noop, n, ("x",), {}),
        number=qtd_execucoes
    )
    print(f"tempo médio de {qtd_execucoes}: {tempo:.4f}s total | {tempo/qtd_execucoes*1000:.4f}ms por chamada")
else:
    _T = float(os.environ["BENCH_DURACAO"])
    _bench = timeit.Timer(lambda: repete(_noop, n, ("x",), {}))
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
