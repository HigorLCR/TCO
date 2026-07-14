"""
Gera recursive_functions/benchmark_tempo/ a partir de .../benchmark/.

Cada script do benchmark mede tempo com um numero FIXO de iteracoes:
    tempo = timeit.timeit(lambda: f(...), number=qtd_execucoes)
    print("tempo medio de N: ...")

Aqui trocamos so o DRIVER: em vez de N iteracoes -> mede tempo, rodamos a MESMA
chamada por ~BENCH_DURACAO segundos (env, padrao 3) e contamos quantas execucoes
cabem no tempo, normalizando para float:
    execucoes = K * (DURACAO / tempo_real)

O corpo das funcoes e o setup da entrada ficam INTACTOS -- ja sao repetiveis
(o timeit original ja chamava o lambda N vezes, entao cada chamada e independente:
input mutavel usa copia/reconstrucao, fib_memo cria memo novo por chamada, etc.).

Scripts sem timeit(lambda: ...) (ex.: manipula_no_expression) sao copiados como
estao -- nao ha chamada para medir por tempo.

Uso:
    python scripts/gerar_benchmark_tempo.py
"""

import ast
from pathlib import Path

BASE = Path(__file__).parent.parent
ORIG = BASE / "recursive_functions" / "benchmark"
DEST = BASE / "recursive_functions" / "benchmark_tempo"

DRIVER = '''

# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(__LAMBDA__)
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
'''


def achar_lambda(tree, src):
    """(lambda_src, lineno_do_stmt) do timeit.timeit(lambda: ...), ou None."""
    for stmt in tree.body:
        for node in ast.walk(stmt):
            if not isinstance(node, ast.Call):
                continue
            f = node.func
            is_timeit = (isinstance(f, ast.Attribute) and f.attr == "timeit") or \
                        (isinstance(f, ast.Name) and f.id == "timeit")
            if not is_timeit:
                continue
            cands = list(node.args) + [k.value for k in node.keywords if k.arg == "stmt"]
            for a in cands:
                if isinstance(a, ast.Lambda):
                    return ast.get_source_segment(src, a), stmt.lineno
    return None


def main() -> None:
    DEST.mkdir(parents=True, exist_ok=True)
    convertidos = copiados = 0
    for p in sorted(ORIG.glob("*.py")):
        src = p.read_text(encoding="utf-8")
        try:
            achado = achar_lambda(ast.parse(src), src)
        except SyntaxError:
            achado = None

        if achado is None:
            (DEST / p.name).write_text(src, encoding="utf-8")
            copiados += 1
            print(f"  [copiado sem timeit] {p.name}")
            continue

        lam_src, cut = achado
        # mantem tudo antes do statement do timeit; remove blanks e o
        # 'qtd_execucoes = ...' orfao no fim (so era usado pelo timeit/print).
        cabeca = p.read_text(encoding="utf-8").splitlines()[:cut - 1]
        while cabeca and (not cabeca[-1].strip()
                          or cabeca[-1].lstrip().startswith("qtd_execucoes")):
            cabeca.pop()
        novo = "\n".join(cabeca).rstrip() + "\n" + DRIVER.replace("__LAMBDA__", lam_src)
        (DEST / p.name).write_text(novo, encoding="utf-8")
        convertidos += 1
        print(f"  [convertido] {p.name:<42} <- {lam_src}")

    print(f"\nConvertidos: {convertidos} | copiados (sem timeit): {copiados}")
    print(f"Destino: {DEST}")


if __name__ == "__main__":
    main()
