"""
Gera xlsx/tempos_execucao.xlsx com a pagina 'Tempos_Execucao', reaproveitando a
ESTRUTURA da aba 'Tempos_Execucao_v4' (cabecalhos descritivos, tabela/estilo e as
linhas manuais 'notacao'/'Complexidade de resolucao'/'Obs') como template, e
atualizando apenas os DADOS calculados a partir de benchmark_results.csv e dos
parametros reais usados nos benchmarks.

Linhas atualizadas (localizadas pelo ROTULO na coluna A):
    Tempo_Recursao_Media       <- <nome>.py           (recursivo)         [sempre]
    Tempo_Iteracao_Tail_Media  <- output_<nome>.py    (tail)              [so quem tem]
    Tempo_Iteracao_Media       <- <nome>_nonrec.py    (nonrec)            [sempre]
    Sobrecarga_Tail...         = formula rec/tail   (por rotulo)          [sempre]
    Sobrecarga...              = formula rec/nonrec (por rotulo)          [sempre]
    Numero_Iteracoes           <- qtd_execucoes do benchmark              [sempre]
    Parametros                 <- args reais no timeit(lambda: f(...))    [sempre]

Preservado do template (nao tocado):
    linha 1 (cabecalhos descritivos), 'Complexidade de resolucao', 'Obs', a
    tabela/estilo, e a tail de quem NAO tem output_ (ex.: 'futuro').

Removido do output: a linha 'notacao' (a tabela e encolhida junto).

Template: ling_rec.xlsx se existir; senao ling_rec_backup_nos.xlsx.
Metrica de tempo: tempo_ms_por_chamada. Valores ausentes viram '-'.

Uso:
    python scripts/gen_tempos_execucao.py
"""

import ast
import csv
import re
import sys
from pathlib import Path

import openpyxl
from openpyxl.utils import get_column_letter, range_boundaries

BASE = Path(__file__).parent.parent
SAIDA_DIR = BASE / "xlsx"  # diretorio padrao de saida dos xlsx gerados
SAIDA = SAIDA_DIR / "tempos_execucao.xlsx"
CSV = BASE / "benchmark_results.csv"
BENCH = BASE / "recursive_functions" / "benchmark"

LING = BASE / "ling_rec.xlsx"
BACKUP = BASE / "ling_rec_backup_nos.xlsx"
ABA_ORIGEM = "Tempos_Execucao_v4"  # aba-template
ABA = "Tempos_Execucao"            # aba de saida

# coluna da planilha -> nome base do arquivo (stem) no CSV
COLUNA_PARA_BASE = {
    "B": "fibonacci",
    "C": "factorial",
    "D": "sum",
    "E": "mdc",
    "F": "woodcutter",
    "G": "binary_search",
    "H": "quickselect",
    "I": "identical_strings",
    "J": "linear_search",
    "K": "non_negative_int_contain_digit",
    "L": "Hannoi",
    "M": "MergeSort",
    "N": "NumSearchTree",
    "O": "fast_pow",
    "P": "count_bits",
    "Q": "flatten",
    "R": "first_missing",
    "S": "valid_bst",
    "T": "fib_memo",
    "U": "countdown",
    "V": "safe_parse",
    "W": "sum_nested",
    "X": "remove_keys",
    "Y": "find_first",
    "Z": "count_matches",
}

# Rotulos das linhas de tempo (usados pelas formulas via MATCH na coluna A)
ROTULO_REC = "Tempo_Recursao_Media"
ROTULO_TAIL = "Tempo_Iteracao_Tail_Media"
ROTULO_NONREC = "Tempo_Iteracao_Media"
LABEL_ITER = "Numero_Iteracoes"
LABEL_PARAMS = "Parametros"
PREFIXO_SOB_TAIL = "Sobrecarga_Tail"  # rotulo comeca assim
PREFIXO_SOB = "Sobrecarga ("          # rotulo comeca assim (distingue do _Tail)


def _formula_sobrecarga(rotulo_denominador: str) -> str:
    """Sobrecarga = (linha rec) / (linha denominador), localizadas pelo rotulo.

    INDEX($A:$AA, MATCH(rotulo, $A:$A, 0), COLUMN()) pega o valor na coluna
    atual da linha cujo rotulo (coluna A) casa exatamente -> imune a
    insercao/reordenacao de linhas.
    """
    num = f'INDEX($A:$AA,MATCH("{ROTULO_REC}",$A:$A,0),COLUMN())'
    den = f'INDEX($A:$AA,MATCH("{rotulo_denominador}",$A:$A,0),COLUMN())'
    return f'=IFERROR(ROUND({num}/{den},3),"-")'


FORMULA_SOB_TAIL = _formula_sobrecarga(ROTULO_TAIL)
FORMULA_SOB = _formula_sobrecarga(ROTULO_NONREC)


def carregar_csv() -> dict[str, dict]:
    """Mapeia nome_do_arquivo -> linha do CSV."""
    dados = {}
    with open(CSV, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            dados[row["arquivo"]] = row
    return dados


def valor(dados: dict, arquivo: str):
    """Retorna o tempo_ms_por_chamada (float) ou None se nao existir/sem timing."""
    row = dados.get(arquivo)
    if row is None or row["status"] != "ok" or not row["tempo_ms_por_chamada"]:
        return None
    return float(row["tempo_ms_por_chamada"])


def qtd_iter(dados: dict, base: str):
    """qtd_execucoes da funcao (rec, depois tail, depois nonrec). None se ausente."""
    for arq in (f"{base}.py", f"output_{base}.py", f"{base}_nonrec.py"):
        row = dados.get(arq)
        if row and row["status"] == "ok" and row["qtd_execucoes"]:
            return int(row["qtd_execucoes"])
    return None


# ----- extracao de parametros dos arquivos de benchmark -----

def _assignments(tree):
    """Mapa nome -> AST do valor das atribuicoes de nivel de modulo."""
    amap = {}
    for node in tree.body:
        if isinstance(node, ast.Assign):
            for t in node.targets:
                if isinstance(t, ast.Name):
                    amap[t.id] = node.value
    return amap


def _substitute(node, amap, depth=0):
    """Substitui Names de modulo pelos seus valores (recursivo, limitado)."""
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
    """Retorna o ast.Call dentro do lambda passado ao timeit, ou None."""
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
    """Encurta literais inteiros longos: 1234...7890(NN dig)."""
    def repl(m):
        s = m.group()
        return f"{s[:6]}...{s[-6:]}({len(s)}dig)"
    return re.sub(r"\d{16,}", repl, texto)


def parametros_de(base: str) -> str:
    """Parametros reais do benchmark recursivo de `base`, formatados 'p1, p2, ...'."""
    arq = BENCH / f"{base}.py"
    if not arq.exists():
        return "-"
    try:
        tree = ast.parse(arq.read_text(encoding="utf-8"))
    except SyntaxError:
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


def mapa_rotulos(ws) -> dict[str, int]:
    """{rotulo_exato_da_coluna_A: linha} para localizar linhas por nome."""
    m = {}
    for r in range(1, ws.max_row + 1):
        v = ws.cell(r, 1).value
        if isinstance(v, str) and v.strip():
            m.setdefault(v.strip(), r)
    return m


def achar(ws, rotulos: dict[str, int], exato: str = None, prefixo: str = None):
    """Linha cujo rotulo casa exatamente (exato) ou comeca com (prefixo)."""
    if exato is not None and exato in rotulos:
        return rotulos[exato]
    if prefixo is not None:
        for rot, r in rotulos.items():
            if rot.startswith(prefixo):
                return r
    return None


def _ajustar_tabelas(ws, linha_removida: int) -> None:
    """Corrige o ref das tabelas apos deletar uma linha (openpyxl nao faz isso).

    - linha acima da tabela  -> desloca inicio e fim uma linha para cima.
    - linha dentro da tabela  -> encolhe o fim em uma linha.
    - linha abaixo da tabela  -> sem efeito.
    """
    for nome in list(ws.tables):
        t = ws.tables[nome]
        min_c, min_r, max_c, max_r = range_boundaries(t.ref)
        if linha_removida < min_r:
            min_r -= 1
            max_r -= 1
        elif min_r <= linha_removida <= max_r:
            max_r -= 1
        t.ref = f"{get_column_letter(min_c)}{min_r}:{get_column_letter(max_c)}{max_r}"


def remover_linha(ws, prefixo: str) -> int | None:
    """Deleta a 1a linha cujo rotulo (coluna A) comeca com `prefixo` (case-insensitive).

    Ajusta as tabelas em seguida. Devolve o indice removido, ou None se nao achou.
    """
    p = prefixo.strip().lower()
    for r in range(1, ws.max_row + 1):
        v = ws.cell(r, 1).value
        if isinstance(v, str) and v.strip().lower().startswith(p):
            ws.delete_rows(r, 1)
            _ajustar_tabelas(ws, r)
            return r
    return None


def main() -> None:
    template = LING if LING.exists() else BACKUP
    if not template.exists():
        print(f"Template nao encontrado (nem {LING.name} nem {BACKUP.name}).")
        sys.exit(1)

    dados = carregar_csv()
    wb = openpyxl.load_workbook(template)
    if ABA_ORIGEM not in wb.sheetnames:
        print(f"Aba '{ABA_ORIGEM}' nao existe em {template.name}. Abas: {wb.sheetnames}")
        sys.exit(1)

    # mantem so a aba-template e renomeia para a aba de saida
    for nome in list(wb.sheetnames):
        if nome != ABA_ORIGEM:
            del wb[nome]
    ws = wb[ABA_ORIGEM]
    ws.title = ABA

    # localiza as linhas de dados pelo rotulo (coluna A)
    rot = mapa_rotulos(ws)
    r_rec = achar(ws, rot, exato=ROTULO_REC)
    r_tail = achar(ws, rot, exato=ROTULO_TAIL)
    r_nonrec = achar(ws, rot, exato=ROTULO_NONREC)
    r_sob_tail = achar(ws, rot, prefixo=PREFIXO_SOB_TAIL)
    r_sob = achar(ws, rot, prefixo=PREFIXO_SOB)
    r_iter = achar(ws, rot, exato=LABEL_ITER)
    r_params = achar(ws, rot, exato=LABEL_PARAMS)
    faltando = [n for n, r in {
        ROTULO_REC: r_rec, ROTULO_TAIL: r_tail, ROTULO_NONREC: r_nonrec,
        PREFIXO_SOB_TAIL: r_sob_tail, PREFIXO_SOB: r_sob,
        LABEL_ITER: r_iter, LABEL_PARAMS: r_params}.items() if r is None]
    if faltando:
        print(f"Rotulos nao encontrados na coluna A: {faltando}")
        sys.exit(1)

    print(f"Template: {template.name}  (linhas rec={r_rec} tail={r_tail} "
          f"nonrec={r_nonrec} iter={r_iter} params={r_params})")
    print(f"{'col':>3} {'funcao':<32} {'rec':>10} {'tail':>10} {'nonrec':>10} {'iter':>8}  parametros")
    print("-" * 110)

    for col, base in COLUNA_PARA_BASE.items():
        rec = valor(dados, f"{base}.py")
        nonrec = valor(dados, f"{base}_nonrec.py")
        tail = valor(dados, f"output_{base}.py")
        iteracoes = qtd_iter(dados, base)
        params = parametros_de(base)

        # recursivo / nonrec: sempre atualiza
        ws[f"{col}{r_rec}"] = rec if rec is not None else "-"
        ws[f"{col}{r_nonrec}"] = nonrec if nonrec is not None else "-"
        # tail: atualiza SO quem tem output_; senao preserva o template ('futuro'/etc.)
        if tail is not None:
            ws[f"{col}{r_tail}"] = tail
        # formulas de sobrecarga (por rotulo, robustas a '-')
        ws[f"{col}{r_sob_tail}"] = FORMULA_SOB_TAIL
        ws[f"{col}{r_sob}"] = FORMULA_SOB
        # numero de iteracoes / parametros
        ws[f"{col}{r_iter}"] = iteracoes if iteracoes is not None else "-"
        ws[f"{col}{r_params}"] = params

        srec = f"{rec:.4f}" if rec is not None else "-"
        stail = f"{tail:.4f}" if tail is not None else "(preservado)"
        snon = f"{nonrec:.4f}" if nonrec is not None else "-"
        siter = str(iteracoes) if iteracoes is not None else "-"
        pshow = params if len(params) <= 40 else params[:37] + "..."
        print(f"{col:>3} {base:<32} {srec:>10} {stail:>10} {snon:>10} {siter:>8}  {pshow}")

    # remove a linha 'notacao' do output (a pedido); encolhe a tabela junto
    removida = remover_linha(ws, "nota")

    SAIDA_DIR.mkdir(exist_ok=True)
    wb.save(SAIDA)

    print("-" * 110)
    print(f"Arquivo criado : {SAIDA}")
    print(f"Aba            : {ABA} (template: {ABA_ORIGEM})")
    print(f"Funcoes        : {len(COLUNA_PARA_BASE)} (colunas B..{list(COLUNA_PARA_BASE)[-1]})")
    print(f"Linha 'notacao': {'removida (era row ' + str(removida) + ')' if removida else 'nao encontrada'}")
    print("Preservado     : cabecalhos, complexidade/obs, tabela/estilo, tail sem output_.")


if __name__ == "__main__":
    main()
