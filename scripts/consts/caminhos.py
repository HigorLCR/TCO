"""
Caminhos do projeto: UMA definicao por arquivo/diretorio, para os scripts nao
repetirem `BASE / "arquivos" / ...` cada um do seu jeito.

Onde um script grava e outro le (o CSV do benchmark, a matriz de nos), a
constante daqui e o contrato entre os dois.
"""

from pathlib import Path

# este modulo vive em scripts/consts/, entao a raiz do projeto sobe 3 niveis
BASE = Path(__file__).resolve().parent.parent.parent
SCRIPTS = BASE / "scripts"

# fontes analisados/medidos
BENCH = BASE / "recursive_functions" / "benchmark"

# worker do benchmark, rodado em subprocesso pelo benchmark.py
WORKER = SCRIPTS / "benchmark_worker.py"

ARQUIVOS = BASE / "arquivos"
CSV_DIR = ARQUIVOS / "csv"
TXT_DIR = ARQUIVOS / "txt"
XLSX_DIR = ARQUIVOS / "xlsx"

# fluxo do benchmark: benchmark.py mede -> CSV -> planilha_tempos.py apresenta
ARQUIVO_CSV = CSV_DIR / "benchmark_results.csv"
ARQUIVO_CSV_TEMPO = CSV_DIR / "execucoes_por_tempo.csv"
XLSX_TEMPOS = XLSX_DIR / "tempos_execucao.xlsx"

# fluxo da cobertura: cobertura.py analisa -> matriz -> planilha_cobertura.py apresenta
MATRIZ_NOS = TXT_DIR / "node_matrix.txt"
XLSX_COBERTURA = XLSX_DIR / "nos_ast_cobertos.xlsx"
