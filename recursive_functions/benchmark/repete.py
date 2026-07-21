import sys
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

# --- benchmark ---
def chamada():
    return repete(_noop, n, ("x",), {})
