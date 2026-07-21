"""
Nomes de arquivo das tres versoes de uma funcao-base, aplicando a convencao
definida em consts/nomes.py.

Existe para ninguem remontar 'output_' + base + '.py' na mao: quem precisa das
tres versoes pede aqui e recebe na ordem de exibicao.
"""

from typing import NamedTuple

from consts.nomes import EXT_PY, PREFIXO_OUTPUT, SUFIXO_NONREC


class Versoes(NamedTuple):
    """Nomes de arquivo das tres versoes, na ordem de exibicao."""
    recursivo: str
    output: str
    nonrec: str


def versoes_de(base: str) -> Versoes:
    """'sum' -> Versoes('sum.py', 'output_sum.py', 'sum_nonrec.py')."""
    return Versoes(
        f"{base}{EXT_PY}",
        f"{PREFIXO_OUTPUT}{base}{EXT_PY}",
        f"{base}{SUFIXO_NONREC}{EXT_PY}",
    )
