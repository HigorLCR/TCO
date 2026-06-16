"""
Executa todos os scripts de benchmark em um diretorio e coleta os tempos.

Uso:
    python scripts/run_benchmarks.py [diretorio] [--output arquivo.csv] [--timeout segundos]

Padrao: recursive_functions/benchmark/
Saida:  benchmark_results.csv (na raiz do projeto)
"""

import csv
import re
import subprocess
import sys
from pathlib import Path

TIMING_RE = re.compile(
    r"tempo m[eé]dio de (\d+):\s*([\d.]+)s total \| ([\d.]+)ms por chamada"
)

SEP = "=" * 70


def classify(name: str) -> str:
    if name.startswith("output_"):
        return "output"
    if name.endswith("_nonrec.py"):
        return "nonrec"
    return "recursivo"


def run_script(path: Path, timeout: int) -> dict:
    base = {
        "arquivo": path.name,
        "tipo": classify(path.name),
        "qtd_execucoes": "",
        "tempo_total_s": "",
        "tempo_ms_por_chamada": "",
        "status": "",
    }
    try:
        proc = subprocess.run(
            [sys.executable, str(path)],
            capture_output=True,
            text=True,
            timeout=timeout,
        )
        output = proc.stdout + proc.stderr
        match = TIMING_RE.search(output)
        if match:
            linha = (f"tempo medio de {match.group(1)}: "
                     f"{match.group(2)}s total | "
                     f"{match.group(3)}ms por chamada")
            base.update({
                "qtd_execucoes": int(match.group(1)),
                "tempo_total_s": float(match.group(2)),
                "tempo_ms_por_chamada": float(match.group(3)),
                "linha": linha,
                "status": "ok",
            })
        elif proc.returncode != 0:
            erro = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "erro desconhecido"
            base["status"] = f"erro: {erro[:80]}"
        else:
            base["status"] = "sem_timing"
    except subprocess.TimeoutExpired:
        base["status"] = f"timeout (>{timeout}s)"
    except Exception as e:
        base["status"] = f"excecao: {e}"
    return base


def run(directory: Path, output_file: Path, timeout: int) -> None:
    files = sorted(
        f for f in directory.iterdir()
        if f.is_file() and f.suffix == ".py"
    )

    if not files:
        print(f"Nenhum arquivo .py encontrado em: {directory}")
        return

    print(f"\n{SEP}")
    print(f"  Diretorio : {directory}")
    print(f"  Arquivos  : {len(files)}")
    print(f"  Timeout   : {timeout}s por script")
    print(SEP)

    results = []
    ok = erros = sem_timing = 0

    for i, f in enumerate(files, 1):
        print(f"  [{i:>2}/{len(files)}] {f.name}", flush=True)
        row = run_script(f, timeout)
        results.append(row)

        if row["status"] == "ok":
            print(f"           {row['linha']}\n")
            ok += 1
        elif row["status"] == "sem_timing":
            print("           (sem linha de timing)\n")
            sem_timing += 1
        else:
            print(f"           {row['status']}\n")
            erros += 1

    fieldnames = ["arquivo", "tipo", "qtd_execucoes", "tempo_total_s", "tempo_ms_por_chamada", "status"]
    with open(output_file, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"\n{SEP}")
    print(f"  Resultado : {ok} ok | {sem_timing} sem timing | {erros} erros")
    print(f"  Salvo em  : {output_file}")
    print(SEP)

    tipos = ["recursivo", "nonrec", "output"]
    print("\nMedia por tipo (scripts com timing):\n")
    for tipo in tipos:
        grupo = [r for r in results if r["tipo"] == tipo and r["status"] == "ok"]
        if grupo:
            media = sum(r["tempo_ms_por_chamada"] for r in grupo) / len(grupo)
            print(f"  {tipo:<12} {len(grupo):>2} scripts   media: {media:.4f} ms/chamada")


if __name__ == "__main__":
    base = Path(__file__).parent.parent  # sobe de scripts/ para raiz do projeto

    args = sys.argv[1:]
    directory = base / "recursive_functions" / "benchmark"
    output_file = base / "benchmark_results.csv"
    timeout = 120

    i = 0
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            output_file = Path(args[i + 1])
            i += 2
        elif args[i] == "--timeout" and i + 1 < len(args):
            timeout = int(args[i + 1])
            i += 2
        else:
            directory = Path(args[i])
            if not directory.is_absolute():
                directory = base / directory
            i += 1

    if not directory.is_dir():
        print(f"Diretorio nao encontrado: {directory}")
        sys.exit(1)

    run(directory, output_file, timeout)
