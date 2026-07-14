"""
Benchmark orientado por TEMPO (analogo ao benchmark.py, mas ao contrario):
em vez de fixar o numero de iteracoes e medir o tempo, aqui fixamos uma
DURACAO (ex.: 3 s) e coletamos QUANTAS execucoes cabem nesse tempo (float).

Duas fases:

  FASE 1 - VERIFICACAO: agrupa as versoes de cada funcao (normal | output_ |
    _nonrec) e confere que usam a MESMA entrada e produzem a MESMA saida (1
    chamada, timeit neutralizado). Garante que a comparacao e justa.

  FASE 2 - MEDICAO POR TEMPO: para cada script, reaproveita o proprio
    timeit.timeit(lambda: f(...)) do arquivo (interceptado em runtime) e roda
    a chamada em lotes por ~DURACAO segundos, contando as execucoes. Reporta
    execucoes_em_T = K * (DURACAO / E), onde K = chamadas medidas e E = tempo
    real gasto (E >~ DURACAO). Grava arquivos/csv/execucoes_por_tempo.csv.

NAO altera nenhum arquivo do benchmark: o callable medido e exatamente o mesmo
que o script ja passa ao timeit.

Uso:
    python scripts/benchmark_por_tempo.py [diretorio] [--duracao seg] [--timeout seg]
    python scripts/benchmark_por_tempo.py --saida <arquivo>          (uso interno)
    python scripts/benchmark_por_tempo.py --tempo <arquivo> <dur>    (uso interno)

Padrao: recursive_functions/benchmark/  |  duracao 3 s  |  timeout 300 s
"""

import ast
import contextlib
import csv
import hashlib
import io
import os
import re
import runpy
import subprocess
import sys
import timeit
from collections import defaultdict
from pathlib import Path

BASE = Path(__file__).parent.parent
THIS = Path(__file__).resolve()
BENCH = BASE / "recursive_functions" / "benchmark"
CSV_OUT = BASE / "arquivos" / "csv" / "execucoes_por_tempo.csv"

SEP = "=" * 70
ORDEM_TIPO = {"recursivo": 0, "output": 1, "nonrec": 2}


def classify(name: str) -> str:
    if name.startswith("output_"):
        return "output"
    if name.endswith("_nonrec.py"):
        return "nonrec"
    return "recursivo"


def base_de(name: str) -> str:
    """Funcao-base: tira '.py', prefixo 'output_' e sufixo '_nonrec'."""
    stem = name[:-3] if name.endswith(".py") else name
    if stem.startswith("output_"):
        stem = stem[len("output_"):]
    if stem.endswith("_nonrec"):
        stem = stem[:-len("_nonrec")]
    return stem


# ==================== extracao da ENTRADA (AST, estatica) ====================

def _assignments(tree):
    amap = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    amap[t.id] = node.value
    return amap


def _substitute(node, amap, depth=0):
    if depth > 4:
        return node

    class R(ast.NodeTransformer):
        def visit_Name(self, n):
            if n.id in amap:
                return _substitute(
                    ast.parse(ast.unparse(amap[n.id]), mode="eval").body, amap, depth + 1)
            return n

    return R().visit(node)


def _achar_timeit_lambda(tree):
    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            f = node.func
            is_timeit = (isinstance(f, ast.Attribute) and f.attr == "timeit") or \
                        (isinstance(f, ast.Name) and f.id == "timeit")
            if not is_timeit:
                continue
            candidatos = list(node.args) + [k.value for k in node.keywords if k.arg == "stmt"]
            for a in candidatos:
                if isinstance(a, ast.Lambda) and isinstance(a.body, ast.Call):
                    return a.body
    return None


def _abreviar_numeros(texto: str) -> str:
    def repl(m):
        s = m.group()
        return f"{s[:6]}...{s[-6:]}({len(s)}dig)"
    return re.sub(r"\d{16,}", repl, texto)


def entrada_de(path: Path) -> str:
    """Args reais da chamada no timeit, resolvidos e formatados 'p1, p2, ...'."""
    try:
        tree = ast.parse(path.read_text(encoding="utf-8"))
    except (SyntaxError, OSError):
        return "-"
    amap = _assignments(tree)
    call = _achar_timeit_lambda(tree)
    if call is None:
        return "-"
    partes = []
    for a in call.args:
        partes.append(_abreviar_numeros(ast.unparse(_substitute(a, amap))))
    for kw in call.keywords:
        partes.append(f"{kw.arg}={_abreviar_numeros(ast.unparse(_substitute(kw.value, amap)))}")
    return ", ".join(partes) if partes else "-"


# ==================== harness: captura da SAIDA (verificacao) ====================

def _canonical(v, depth=0) -> str:
    """Representacao canonica SEM endereco de memoria, para comparar saidas."""
    if depth > 8:
        return "..."
    if isinstance(v, ast.AST):
        return ast.dump(v)
    if isinstance(v, (list, tuple)):
        abre, fecha = ("[", "]") if isinstance(v, list) else ("(", ")")
        return abre + ",".join(_canonical(x, depth + 1) for x in v) + fecha
    if isinstance(v, dict):
        return "{" + ",".join(
            f"{_canonical(k, depth + 1)}:{_canonical(val, depth + 1)}" for k, val in v.items()) + "}"
    if isinstance(v, (set, frozenset)):
        return "{" + ",".join(sorted(_canonical(x, depth + 1) for x in v)) + "}"
    r = repr(v)
    if " object at 0x" in r and hasattr(v, "__dict__"):
        return f"{type(v).__name__}({_canonical(vars(v), depth + 1)})"
    return r


def _harness_saida(path_str: str) -> None:
    """Executa `path` com timeit neutralizado (1 chamada) e emite __OUTPUT__."""
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    path = Path(path_str)
    real = timeit.timeit
    cap = {}

    def patched(stmt="pass", setup="pass", timer=timeit.default_timer,
                number=1000000, globals=None):
        if callable(stmt):
            try:
                cap["out"] = stmt()
            except Exception as e:
                cap["err"] = f"{type(e).__name__}: {e}"
        return 0.0

    timeit.timeit = patched
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            runpy.run_path(str(path), run_name="__main__")
    except Exception as e:
        print(f"__OUTPUT__\tERRO\t{type(e).__name__}: {e}")
        return
    finally:
        timeit.timeit = real

    if "err" in cap:
        print(f"__OUTPUT__\tERRO\t{cap['err']}")
    elif "out" in cap:
        r = _canonical(cap["out"])
        h = hashlib.md5(r.encode("utf-8", "replace")).hexdigest()[:10]
        preview = r if len(r) <= 70 else r[:67] + "..."
        print(f"__OUTPUT__\t{h}\t{preview.replace(chr(9), ' ').replace(chr(10), ' ')}")
    else:
        print("__OUTPUT__\tn/d\t(sem chamada timeit detectada)")


# ==================== harness: medicao por TEMPO ====================

def _harness_tempo(path_str: str, duracao: float) -> None:
    """Roda a chamada do script em lotes por ~duracao s e emite __EXEC__.

    Intercepta o timeit.timeit do script para pegar o mesmo callable
    (lambda: f(...)). Usa timeit.Timer (timing real, em lote) para nao ter
    overhead por chamada. Emite: status, execucoes(float), K(chamadas), E(s).
    """
    if hasattr(sys, "set_int_max_str_digits"):
        sys.set_int_max_str_digits(0)
    path = Path(path_str)
    real = timeit.timeit
    cap = {}

    def patched(stmt="pass", setup="pass", timer=timeit.default_timer,
                number=1000000, globals=None):
        if not callable(stmt):
            return 0.0
        try:
            t = timeit.Timer(stmt)          # Timer usa timing real (nao o patched)
            n_cal, t_cal = t.autorange()    # calibra: acha lote com t_cal >= 0.2s
            if t_cal >= duracao:
                k, e = n_cal, t_cal         # a calibracao ja passou de T: usa ela
            else:
                por_chamada = t_cal / n_cal
                alvo = max(1, round(duracao / por_chamada))
                e = t.timeit(number=alvo)   # roda ~duracao segundos
                k = alvo
            cap["exec"] = k * (duracao / e)  # normaliza para exatamente `duracao`
            cap["k"] = k
            cap["e"] = e
        except Exception as ex:
            cap["err"] = f"{type(ex).__name__}: {ex}"
        return 0.0

    timeit.timeit = patched
    buf = io.StringIO()
    try:
        with contextlib.redirect_stdout(buf):
            runpy.run_path(str(path), run_name="__main__")
    except Exception as ex:
        print(f"__EXEC__\tERRO\t0\t0\t0\t{type(ex).__name__}: {ex}")
        return
    finally:
        timeit.timeit = real

    if "err" in cap:
        print(f"__EXEC__\tERRO\t0\t0\t0\t{cap['err']}")
    elif "exec" in cap:
        print(f"__EXEC__\tOK\t{cap['exec']:.6f}\t{cap['k']}\t{cap['e']:.6f}\t")
    else:
        print("__EXEC__\tNAO\t0\t0\t0\t(sem chamada timeit detectada)")


# ==================== FASE 1: verificacao ====================

def _saida_de(path: Path, timeout: int) -> tuple[str, str]:
    try:
        proc = subprocess.run(
            [sys.executable, str(THIS), "--saida", str(path)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        return "TIMEOUT", f"(>{timeout}s)"
    m = re.search(r"^__OUTPUT__\t(\S+)\t(.*)$", proc.stdout, re.MULTILINE)
    if m:
        return m.group(1), m.group(2)
    ultimo = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "sem saida"
    return "ERRO", ultimo[:70]


def fase_verificacao(files: list[Path], timeout: int) -> int:
    print(f"\n{SEP}\n  FASE 1 - VERIFICACAO (entrada e saida das versoes)\n{SEP}\n")

    resultados = []
    for i, f in enumerate(files, 1):
        print(f"  [{i:>2}/{len(files)}] {f.name}", flush=True)
        h, prev = _saida_de(f, timeout)
        resultados.append({
            "arquivo": f.name, "tipo": classify(f.name), "base": base_de(f.name),
            "entrada": entrada_de(f), "saida_hash": h, "saida_preview": prev,
        })

    por_base = defaultdict(list)
    for r in resultados:
        por_base[r["base"]].append(r)

    print(f"\n{SEP}\n  Comparacao por funcao (normal | output_ | _nonrec)\n{SEP}\n")
    iguais = divergentes = sozinhas = 0
    for base in sorted(por_base):
        versoes = sorted(por_base[base], key=lambda v: ORDEM_TIPO.get(v["tipo"], 9))
        entradas = {v["entrada"] for v in versoes}
        hashes = {v["saida_hash"] for v in versoes}
        bons = all(v["saida_hash"] not in ("ERRO", "TIMEOUT", "n/d") for v in versoes)
        ent_ok = len(entradas) == 1
        sai_ok = bons and len(hashes) == 1

        if len(versoes) < 2:
            sozinhas += 1
            veredito = "(1 versao, nada a comparar)"
        elif ent_ok and sai_ok:
            iguais += 1
            veredito = "OK  (entrada e saida iguais)"
        else:
            divergentes += 1
            sai_txt = "iguais" if sai_ok else ("DIFEREM" if bons else "incompleto")
            veredito = f"DIVERGE  (entrada: {'iguais' if ent_ok else 'DIFEREM'} | saida: {sai_txt})"

        print(f"  {base}  ->  {veredito}")
        if ent_ok:
            print(f"      entrada: {next(iter(entradas))}")
            for v in versoes:
                print(f"        {v['tipo']:<10} {v['arquivo']:<36} saida: {v['saida_hash']} | {v['saida_preview']}")
        else:
            for v in versoes:
                print(f"        {v['tipo']:<10} {v['arquivo']:<36} entrada: {v['entrada']}")
                print(f"        {'':<10} {'':<36} saida  : {v['saida_hash']} | {v['saida_preview']}")
        print()

    print(SEP)
    print(f"  {iguais} OK | {divergentes} divergentes | {sozinhas} sem par")
    print(SEP)
    return divergentes


# ==================== FASE 2: medicao por tempo ====================

def _medir_tempo(path: Path, duracao: float, timeout: int) -> dict:
    row = {
        "arquivo": path.name, "tipo": classify(path.name),
        "duracao_s": duracao, "execucoes": "", "chamadas_medidas": "",
        "tempo_real_s": "", "status": "",
    }
    try:
        proc = subprocess.run(
            [sys.executable, str(THIS), "--tempo", str(path), str(duracao)],
            capture_output=True, text=True, encoding="utf-8", errors="replace",
            timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        row["status"] = f"timeout (>{timeout}s)"
        return row
    m = re.search(r"^__EXEC__\t(\S+)\t(\S+)\t(\d+)\t(\S+)\t(.*)$", proc.stdout, re.MULTILINE)
    if not m:
        ultimo = proc.stderr.strip().splitlines()[-1] if proc.stderr.strip() else "sem saida"
        row["status"] = f"erro: {ultimo[:80]}"
        return row
    status, execucoes, k, e, msg = m.groups()
    if status == "OK":
        row.update({"execucoes": float(execucoes), "chamadas_medidas": int(k),
                    "tempo_real_s": float(e), "status": "ok"})
    elif status == "NAO":
        row["status"] = "sem_timing"
    else:
        row["status"] = f"erro: {msg[:80]}"
    return row


def fase_medicao(files: list[Path], duracao: float, timeout: int) -> dict[str, dict]:
    print(f"\n{SEP}\n  FASE 2 - MEDICAO POR TEMPO ({duracao}s/script)\n{SEP}\n")

    dados = {}
    ok = erros = sem = 0
    for i, f in enumerate(files, 1):
        row = _medir_tempo(f, duracao, timeout)
        dados[f.name] = row
        if row["status"] == "ok":
            print(f"  [{i:>2}/{len(files)}] {f.name:<40} "
                  f"exec {row['execucoes']:>14,.2f}  ({row['chamadas_medidas']} em {row['tempo_real_s']:.3f}s)")
            ok += 1
        elif row["status"] == "sem_timing":
            print(f"  [{i:>2}/{len(files)}] {f.name:<40} (sem timing)")
            sem += 1
        else:
            print(f"  [{i:>2}/{len(files)}] {f.name:<40} {row['status']}")
            erros += 1

    fieldnames = ["arquivo", "tipo", "duracao_s", "execucoes",
                  "chamadas_medidas", "tempo_real_s", "status"]
    CSV_OUT.parent.mkdir(parents=True, exist_ok=True)
    with open(CSV_OUT, "w", newline="", encoding="utf-8") as fp:
        w = csv.DictWriter(fp, fieldnames=fieldnames)
        w.writeheader()
        w.writerows(dados.values())

    print(f"\n  {ok} ok | {sem} sem timing | {erros} erros   ->  {CSV_OUT}")
    return dados


# ==================== orquestracao ====================

def main() -> None:
    args = sys.argv[1:]
    directory = BENCH
    duracao = 3.0
    timeout = 300
    i = 0
    while i < len(args):
        if args[i] == "--duracao" and i + 1 < len(args):
            duracao = float(args[i + 1])
            i += 2
        elif args[i] == "--timeout" and i + 1 < len(args):
            timeout = int(args[i + 1])
            i += 2
        else:
            directory = Path(args[i])
            if not directory.is_absolute():
                directory = BASE / directory
            i += 1

    if not directory.is_dir():
        print(f"Diretorio nao encontrado: {directory}")
        sys.exit(1)

    files = sorted(f for f in directory.iterdir() if f.is_file() and f.suffix == ".py")
    if not files:
        print(f"Nenhum .py em: {directory}")
        sys.exit(1)

    print(f"\n{SEP}\n  BENCHMARK POR TEMPO - {len(files)} arquivos | {duracao}s cada\n{SEP}")

    divergentes = fase_verificacao(files, timeout)
    if divergentes:
        print(f"\n  [AVISO] {divergentes} funcao(oes) com entrada/saida divergente: "
              f"a comparacao delas pode nao ser justa.\n")

    fase_medicao(files, duracao, timeout)

    print(f"\n{SEP}\n  Concluido: verificacao + medicao por tempo\n{SEP}")


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    if len(sys.argv) >= 3 and sys.argv[1] == "--saida":
        _harness_saida(sys.argv[2])
        sys.exit(0)
    if len(sys.argv) >= 4 and sys.argv[1] == "--tempo":
        _harness_tempo(sys.argv[2], float(sys.argv[3]))
        sys.exit(0)

    main()
