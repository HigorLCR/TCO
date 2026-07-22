"""
Pipeline do benchmark, em um unico script e duas fases:

  FASE 1 - VERIFICACAO: para cada funcao, agrupa suas versoes (normal | output_ |
    _nonrec) e confere que usam a MESMA entrada e produzem a MESMA saida (a
    chamada() do arquivo e executada 1x num worker). Assim confirmamos que a
    comparacao de tempos e justa ANTES de medir.

  FASE 2 - BENCHMARK: mede a chamada() de cada arquivo num worker isolado:
    - CLASSICO (padrao): timeit.timeit(chamada, number=N), com N vindo de
      QTD_EXECUCOES (dict central por funcao-base);
      grava arquivos/csv/benchmark_results.csv.
    - POR TEMPO (--duracao T): T e PISO: o worker itera em lotes ate a soma
      dos tempos alcancar >= T s e reporta tempo total, iteracoes exatas e
      ms por chamada; grava arquivos/csv/execucoes_por_tempo.csv.

Os arquivos medidos nao contem logica de benchmark: cada um define a funcao,
as entradas e um `def chamada()` com a chamada medida. Toda a execucao vive em
scripts/benchmark_worker.py, rodado em subprocesso (um por arquivo/operacao) e
respondendo o resultado em JSON. Arquivos sem chamada() saem como sem_chamada.

A planilha (arquivos/xlsx/tempos_execucao.xlsx) e gerada a parte por
scripts/planilha_tempos.py, a partir do CSV do modo classico.

Uso:
    python scripts/benchmark.py [diretorio] [--timeout segundos]
    python scripts/benchmark.py --duracao 3        (modo por tempo, 3 s/script)

Padrao: recursive_functions/benchmark/
"""

import csv
import json
import subprocess
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import NamedTuple

from consts import (
    ARQUIVO_CSV,
    ARQUIVO_CSV_TEMPO,
    BASE,
    BENCH,
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
    EXT_PY,
    PREFIXO_OUTPUT,
    QTD_EXECUCOES,
    SUFIXO_NONREC,
    WORKER,
)
from utils import entrada_de

SEP = "=" * 70

TIMEOUT_PADRAO = 120  # segundos por worker

# ordem de exibicao das versoes de cada funcao
ORDEM_TIPO = {"recursivo": 0, "output": 1, "nonrec": 2}

# ==================== Auxiliares ====================

def classifica(name: str) -> str:
    if name.startswith(PREFIXO_OUTPUT):
        return "output"
    if name.endswith(SUFIXO_NONREC + EXT_PY):
        return "nonrec"
    return "recursivo"


def base_de(name: str) -> str:
    """Funcao-base: tira '.py', prefixo 'output_' e sufixo '_nonrec'."""
    stem = name[:-len(EXT_PY)] if name.endswith(EXT_PY) else name
    if stem.startswith(PREFIXO_OUTPUT):
        stem = stem[len(PREFIXO_OUTPUT):]
    if stem.endswith(SUFIXO_NONREC):
        stem = stem[:-len(SUFIXO_NONREC)]
    return stem


# ==================== chamada do worker (benchmark_worker.py) ====================

def executar(modo: str, path: Path, timeout: int, param=None) -> dict:
    """Roda benchmark_worker.py em subprocesso e devolve o JSON do resultado.

    O worker so escreve o JSON em stdout, entao stdout inteiro e a resposta.
    Se ele morreu antes de responder (ex.: estouro de pilha C, que nem excecao
    vira), o stderr/rc viram o diagnostico.
    """
    cmd = [sys.executable, str(WORKER), modo, str(path)]
    if param is not None:
        cmd.append(str(param))
    try:
        proc = subprocess.run(
            cmd, 
            capture_output=True, 
            text=True, 
            encoding="utf-8",
            errors="replace", 
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return {"status": "timeout", "msg": f">{timeout}s"}

    try:
        return json.loads(proc.stdout)
    except json.JSONDecodeError:
        linhas = proc.stderr.strip().splitlines()
        motivo = linhas[-1] if linhas else f"sem saida (rc={proc.returncode})"
        return {"status": "erro", "msg": motivo[:80]}


# ==================== FASE 1: verificacao ====================

class Saida(NamedTuple):
    """Saida de uma chamada() vista pela verificacao.

    comparavel=False quando nao houve saida (erro, timeout, sem chamada): nesse
    caso hash/preview servem so para o relatorio, nunca para comparar versoes.
    """
    hash: str
    preview: str
    comparavel: bool


class Versao(NamedTuple):
    """Uma versao (normal | output_ | _nonrec) de uma funcao-base."""
    arquivo: str
    tipo: str
    base: str
    entrada: str
    saida: Saida


def coleta_saida(path: Path, timeout: int) -> Saida:
    """Roda o worker 'verificar' e devolve a Saida da chamada() do arquivo."""
    res = executar("verificar", path, timeout)
    match res.get("status", "erro"):
        case "ok":
            return Saida(res["hash"], res["preview"], comparavel=True)
        case "sem_chamada":
            return Saida("n/d", "(sem def chamada())", comparavel=False)
        case "timeout":
            return Saida("TIMEOUT", f"({res['msg']})", comparavel=False)
        case _:
            return Saida("ERRO", res.get("msg", "sem saida")[:70], comparavel=False)


def compara_versao(versoes: list[Versao]) -> tuple[str, str]:
    """Julga um grupo de versoes: devolve (categoria, veredito legivel).

    categoria: 'sozinha' (nada a comparar) | 'igual' | 'divergente'.
    """
    if len(versoes) < 2:
        return "sozinha", "(1 versao, nada a comparar)"

    # utiliza sets para comparar entrada/saida 
    entrada_ok = len({v.entrada for v in versoes}) == 1
    completo = all(v.saida.comparavel for v in versoes)
    saida_ok = completo and len({v.saida.hash for v in versoes}) == 1

    if entrada_ok and saida_ok:
        return "igual", "OK  (entrada e saida iguais)"

    saida_txt = "iguais" if saida_ok else ("DIFEREM" if completo else "incompleto")
    return "divergente", (f"DIVERGE  (entrada: {'iguais' if entrada_ok else 'DIFEREM'}"
                          f" | saida: {saida_txt})")


def printa_grupo(base: str, versoes: list[Versao], veredito: str) -> None:
    """Bloco do relatorio de uma funcao-base; so repete a entrada se ela divergir."""
    print(f"  {base}  ->  {veredito}")
    entradas = {v.entrada for v in versoes}
    entrada_unica = len(entradas) == 1
    if entrada_unica:
        print(f"      entrada: {next(iter(entradas))}")
    for v in versoes:
        if entrada_unica:
            print(f"        {v.tipo:<10} {v.arquivo:<36} saida: {v.saida.hash} | {v.saida.preview}")
        else:
            print(f"        {v.tipo:<10} {v.arquivo:<36} entrada: {v.entrada}")
            print(f"        {'':<10} {'':<36} saida  : {v.saida.hash} | {v.saida.preview}")
    print()


def fase_verificacao(files: list[Path], timeout: int) -> int:
    """Confere entrada/saida entre versoes; imprime relatorio. Devolve nº de divergencias."""
    print(f"\n{SEP}\n  FASE 1 - VERIFICACAO (entrada e saida das versoes)\n{SEP}\n")

    versoes = []
    for i, arquivo in enumerate(files, 1):
        print(f"  [{i:>2}/{len(files)}] {arquivo.name}", flush=True)
        versoes.append(Versao(
            arquivo=arquivo.name,
            tipo=classifica(arquivo.name),
            base=base_de(arquivo.name),
            entrada=entrada_de(arquivo),
            saida=coleta_saida(arquivo, timeout),
        ))

    # agrupa por funcao-base -> {"sum": [sum.py, output_sum.py, sum_nonrec.py], ...}
    por_base = defaultdict(list)
    for v in versoes:
        por_base[v.base].append(v)

    print(f"\n{SEP}\n  Comparacao por funcao (normal | output_ | _nonrec)\n{SEP}\n")
    contagem = Counter()
    for base in sorted(por_base):
        grupo = sorted(por_base[base], key=lambda v: ORDEM_TIPO.get(v.tipo, 9))
        categoria, veredito = compara_versao(grupo)
        contagem[categoria] += 1
        printa_grupo(base, grupo, veredito)

    print(SEP)
    print(f"  {contagem['igual']} OK | {contagem['divergente']} divergentes"
          f" | {contagem['sozinha']} sem par")
    print(SEP)
    return contagem["divergente"]


# ==================== FASE 2: benchmark (classico ou por tempo) ====================

def medir(path: Path, timeout: int, duracao: float | None = None) -> dict:
    """Mede um arquivo no worker e devolve a linha do CSV.

    duracao=None  -> classico: timeit(chamada, number=N), N de QTD_EXECUCOES.
    duracao=T     -> por tempo: o worker itera em lotes ate somar >= T s.
    """
    if duracao is None:
        row = {
            COL_ARQUIVO: path.name, 
            COL_TIPO: classifica(path.name),
            COL_QTD: "", 
            COL_TOTAL_S: "", 
            COL_MS: "", 
            COL_STATUS: "",
        }
        num_iteracoes = QTD_EXECUCOES.get(base_de(path.name), 0)

        res = executar("classico", path, timeout, num_iteracoes)
        if res.get("status") == "ok":
            row.update({
                COL_QTD: res["qtd"],
                COL_TOTAL_S: res["total"],
                COL_MS: res["ms"],
                COL_STATUS: "ok",
            })
    else:
        row = {
            COL_ARQUIVO: path.name, 
            COL_TIPO: classifica(path.name),
            COL_PISO_S: duracao, 
            COL_ITERACOES: "", 
            COL_TOTAL_S: "",
            COL_MS: "", 
            COL_STATUS: "",
        }
        res = executar("tempo", path, timeout, duracao)
        if res.get("status") == "ok":
            row.update({
                COL_ITERACOES: res["iteracoes"],
                COL_TOTAL_S: res["total"],
                COL_MS: res["ms"],
                COL_STATUS: "ok",
            })
    if row[COL_STATUS] != "ok":
        status = res.get("status", "erro")
        row[COL_STATUS] = f"{status}: {res['msg']}" if "msg" in res else status
    return row


def fase_benchmark(
    files: list[Path],
    timeout: int,
    duracao: float | None = None,
) -> dict[str, dict]:
    """Mede (classico ou por tempo), grava o CSV e devolve {arquivo: row}."""

    if duracao is None:
        print(f"\n{SEP}\n  FASE 2 - BENCHMARK (timeit completo)  timeout {timeout}s/script\n{SEP}\n")
        arquivo_csv = ARQUIVO_CSV
        fieldnames = COLUNAS_CSV
    else:
        print(f"\n{SEP}\n  FASE 2 - BENCHMARK POR TEMPO (piso {duracao}s/script)  timeout {timeout}s\n{SEP}\n")
        arquivo_csv = ARQUIVO_CSV_TEMPO
        fieldnames = COLUNAS_CSV_TEMPO

    dados = {}
    ok = erros = sem = 0
    for i, arquivo in enumerate(files, 1):
        row = medir(arquivo, timeout, duracao)
        dados[arquivo.name] = row

        if row[COL_STATUS] == "ok" and duracao is None:
            print(f"  [{i:>2}/{len(files)}] {arquivo.name:<40} "
                  f"qtd {row[COL_QTD]} | {row[COL_MS]:.4f} ms/chamada")
            ok += 1
        elif row[COL_STATUS] == "ok":
            print(f"  [{i:>2}/{len(files)}] {arquivo.name:<40} "
                  f"{row[COL_ITERACOES]:>10} iteracoes | {row[COL_TOTAL_S]:.4f}s total "
                  f"| {row[COL_MS]:.4f} ms/chamada")
            ok += 1
        elif row[COL_STATUS] in ("sem_chamada", "sem_qtd"):
            print(f"  [{i:>2}/{len(files)}] {arquivo.name:<40} ({row[COL_STATUS]})")
            sem += 1
        else:
            print(f"  [{i:>2}/{len(files)}] {arquivo.name:<40} {row[COL_STATUS]}")
            erros += 1

    arquivo_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(arquivo_csv, "w", newline="", encoding="utf-8") as fp:
        w = csv.DictWriter(fp, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(dados.values())

    print(f"\n  {ok} ok | {sem} sem chamada/qtd | {erros} erros   ->  {arquivo_csv}")
    return dados


# ==================== orquestracao ====================

def main() -> None:
    args = sys.argv[1:]
    alvo = BENCH
    timeout = TIMEOUT_PADRAO
    duracao = None
    i = 0
    #coleta de argumentos opcionais
    while i < len(args):
        if args[i] == "--timeout" and i + 1 < len(args):
            timeout = int(args[i + 1])
            i += 2
        elif args[i] == "--duracao" and i + 1 < len(args):
            duracao = float(args[i + 1])
            i += 2
        else:
            alvo = Path(args[i])
            if not alvo.is_absolute():
                alvo = BASE / alvo
            i += 1

    if not alvo.is_dir():
        print(f"Diretorio nao encontrado: {alvo}")
        sys.exit(1)

    files = sorted(f for f in alvo.iterdir() if f.is_file() and f.suffix == EXT_PY)
    if not files:
        print(f"Nenhum .py em: {alvo}")
        sys.exit(1)

    modo = "classico" if duracao is None else f"por tempo ({duracao}s/script)"
    print(f"\n{SEP}\n  BENCHMARK - {len(files)} arquivo(s) em {alvo} | modo {modo}\n{SEP}")

    divergentes = fase_verificacao(files, timeout)
    if divergentes:
        print(f"\n  [AVISO] {divergentes} funcao(oes) com entrada/saida divergente entre "
              f"versoes: a comparacao de tempos delas pode nao ser justa.\n")

    fase_benchmark(files, timeout, duracao)
    if duracao is None:
        print(f"\n{SEP}\n  Concluido: verificacao + benchmark classico "
              f"(planilha: python scripts/planilha_tempos.py)\n{SEP}")
    else:
        print(f"\n{SEP}\n  Concluido: verificacao + benchmark por tempo\n{SEP}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
