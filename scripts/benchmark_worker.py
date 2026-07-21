"""
Worker do benchmark: executa UM arquivo medido e opera sobre a sua chamada().

E sempre rodado em subprocesso pelo scripts/benchmark.py (nunca importado por
ele): o isolamento e o que protege o pai de estouro de pilha, travamento e do
IO dos arquivos medidos.

    python scripts/benchmark_worker.py verificar <arquivo>
    python scripts/benchmark_worker.py classico  <arquivo> <N>
    python scripts/benchmark_worker.py tempo     <arquivo> <T>

Escreve em stdout UMA coisa: o JSON do resultado. O stdout do arquivo medido
(prints de demonstracao, prints dentro da chamada()) e desviado para um buffer
descartavel logo no inicio, entao o pai pode ler stdout inteiro como JSON.
"""

import ast
import hashlib
import io
import json
import sys
import timeit
from pathlib import Path


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


def _carregar_chamada(path: Path):
    """Executa o modulo do arquivo e devolve a sua chamada() (None se nao existir)."""
    sys.path.insert(0, str(path.parent))  # paridade com `python arquivo.py`
    g = {"__name__": "__main__", "__file__": str(path)}
    exec(compile(path.read_text(encoding="utf-8"), str(path), "exec"), g)
    chamada = g.get("chamada")
    return chamada if callable(chamada) else None


def _verificar(chamada) -> dict:
    """Roda 1x e resume a saida em hash md5 + previa legivel."""
    r = _canonical(chamada())
    return {
        "status": "ok",
        "hash": hashlib.md5(r.encode("utf-8", "replace")).hexdigest()[:10],
        "preview": (r if len(r) <= 70 else r[:67] + "...").replace("\t", " ").replace("\n", " "),
    }


def _classico(chamada, n: int) -> dict:
    """timeit com numero fixo de iteracoes."""
    if n <= 0:
        return {"status": "sem_qtd"}  # funcao-base fora de QTD_EXECUCOES
    tempo = timeit.timeit(chamada, number=n)
    return {"status": "ok", "qtd": n, "total": round(tempo, 4), "ms": round(tempo / n * 1000, 4)}


def _por_tempo(chamada, piso: float) -> dict:
    """Lotes de iteracoes completas ate a soma dos tempos alcancar o piso."""
    bench = timeit.Timer(chamada)
    k, soma, lote = 0, 0.0, 1
    while soma < piso:
        soma += bench.timeit(number=lote)
        k += lote
        if soma >= piso:
            break
        estimativa = int((piso - soma) / (soma / k))  # o que falta, pela taxa
        lote = max(1, min(estimativa, lote * 10))
    return {"status": "ok", "iteracoes": k, "total": round(soma, 4),
            "ms": round(soma / k * 1000, 4)}


def operar(modo: str, path: Path, param: str | None) -> dict:
    """Carrega o arquivo e despacha a operacao pedida."""
    chamada = _carregar_chamada(path)
    if chamada is None:
        return {"status": "sem_chamada"}
    if modo == "verificar":
        return _verificar(chamada)
    if modo == "classico":
        return _classico(chamada, int(param))
    return _por_tempo(chamada, float(param))


if __name__ == "__main__":
    sys.set_int_max_str_digits(0)  # nao limita repr/print de inteiros gigantes

    # a partir daqui stdout e do arquivo medido e vai para o lixo; o resultado
    # sai pelo stdout real, guardado antes
    stdout_real = sys.stdout
    sys.stdout = io.StringIO()
    try:
        resultado = operar(
            sys.argv[1], Path(sys.argv[2]), sys.argv[3] if len(sys.argv) > 3 else None)
    except BaseException as e:  # inclui RecursionError e SystemExit do arquivo medido
        resultado = {"status": "erro", "msg": f"{type(e).__name__}: {e}"[:120]}

    print(json.dumps(resultado), file=stdout_real)
