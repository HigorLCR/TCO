"""
Constantes compartilhadas pelos scripts de scripts/.

Existe para que nenhum script precise importar outro: quem gera e quem
apresenta se falam pelo que esta aqui (o caminho do CSV, as colunas dele, a
convencao de nome dos arquivos), nao por import direto. As funcoes
compartilhadas ficam em utils/.

    caminhos.py     onde cada arquivo do projeto fica
    nomes.py        convencao de nome dos arquivos medidos
    formato_csv.py  colunas dos CSVs do benchmark
    execucoes.py    QTD_EXECUCOES: iteracoes do modo classico

    from consts import BENCH, ARQUIVO_CSV, COLUNAS_CSV
"""

from consts.caminhos import (
    ARQUIVO_CSV,
    ARQUIVO_CSV_TEMPO,
    ARQUIVOS,
    BASE,
    BENCH,
    CSV_DIR,
    MATRIZ_NOS,
    SCRIPTS,
    TXT_DIR,
    WORKER,
    XLSX_COBERTURA,
    XLSX_DIR,
    XLSX_TEMPOS,
)
from consts.execucoes import QTD_EXECUCOES
from consts.formato_csv import (
    COL_ARQUIVO,
    COL_ITERACOES,
    COL_MS,
    COL_PISO_S,
    COL_QTD,
    COL_STATUS,
    COL_TIPO,
    COL_TOTAL_S,
    COLUNAS_CSV,
    COLUNAS_CSV_TEMPO,
)
from consts.nomes import EXT_PY, PREFIXO_OUTPUT, SUFIXO_NONREC

__all__ = [
    "ARQUIVO_CSV",
    "ARQUIVO_CSV_TEMPO",
    "ARQUIVOS",
    "BASE",
    "BENCH",
    "COL_ARQUIVO",
    "COL_ITERACOES",
    "COL_MS",
    "COL_PISO_S",
    "COL_QTD",
    "COL_STATUS",
    "COL_TIPO",
    "COL_TOTAL_S",
    "COLUNAS_CSV",
    "COLUNAS_CSV_TEMPO",
    "CSV_DIR",
    "EXT_PY",
    "MATRIZ_NOS",
    "PREFIXO_OUTPUT",
    "QTD_EXECUCOES",
    "SCRIPTS",
    "SUFIXO_NONREC",
    "TXT_DIR",
    "WORKER",
    "XLSX_COBERTURA",
    "XLSX_DIR",
    "XLSX_TEMPOS",
]
