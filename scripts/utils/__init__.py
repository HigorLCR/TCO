"""
Funcoes compartilhadas pelos scripts de scripts/.

Existe pelo mesmo motivo do consts/: para que nenhum script precise importar
outro. Aqui ficam as funcoes; os caminhos e demais constantes ficam em consts.

    from utils import entrada_de
"""

from utils.entrada_ast import entrada_de
from utils.versoes import Versoes, versoes_de

__all__ = ["Versoes", "entrada_de", "versoes_de"]
