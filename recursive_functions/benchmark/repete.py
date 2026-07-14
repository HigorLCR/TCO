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
# Com BENCH_DURACAO=<segundos>: modo POR TEMPO (roda ~T s -> execucoes, float).
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
    _ncal, _tcal = _bench.autorange()      # calibra: lote com _tcal >= 0.2s
    if _tcal >= _T:
        _k, _e = _ncal, _tcal              # a calibracao ja cobriu a duracao
    else:
        _alvo = max(1, round(_T / (_tcal / _ncal)))
        _e = _bench.timeit(number=_alvo)   # roda ~T segundos
        _k = _alvo
    _execucoes = _k * (_T / _e)            # normaliza para exatamente T
    print(f"execucoes em {_T}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
