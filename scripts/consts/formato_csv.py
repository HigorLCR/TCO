"""
Colunas dos CSVs do benchmark — o contrato entre quem grava e quem le.

O benchmark.py escreve essas colunas; o planilha_tempos.py le por nome
(COL_STATUS, COL_MS, COL_QTD). Estao aqui para que renomear uma coluna nao
signifique sair cacando string literal nos dois scripts.
"""

COL_ARQUIVO = "arquivo"
COL_TIPO = "tipo"
COL_STATUS = "status"
COL_QTD = "qtd_execucoes"
COL_TOTAL_S = "tempo_total_s"
COL_MS = "tempo_ms_por_chamada"
COL_PISO_S = "piso_s"
COL_ITERACOES = "iteracoes"

# modo classico -> benchmark_results.csv
COLUNAS_CSV = [COL_ARQUIVO, COL_TIPO, COL_QTD, COL_TOTAL_S, COL_MS, COL_STATUS]

# modo por tempo (--duracao) -> execucoes_por_tempo.csv
COLUNAS_CSV_TEMPO = [COL_ARQUIVO, COL_TIPO, COL_PISO_S, COL_ITERACOES,
                     COL_TOTAL_S, COL_MS, COL_STATUS]
