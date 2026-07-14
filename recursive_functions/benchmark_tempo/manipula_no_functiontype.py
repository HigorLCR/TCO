import sys
import timeit
import ast

sys.setrecursionlimit(10_000)

# Funcao recursiva que manipula um no ast.FunctionType.
# A raiz aqui e um FunctionType (mode="func_type"), que representa um
# "type comment" no formato  (tipos_dos_args) -> tipo_de_retorno.
# Em vez de dobrar constantes (nao ha aritmetica em tipos), a manipulacao
# analoga e renomear recursivamente os nomes de tipo segundo um mapa,
# descendo por tipos genericos aninhados como list[dict[str, int]].


def mapeia_tipos(no, mapa):
    """Recebe e devolve um no, renomeando recursivamente nomes de tipo.

    - ast.FunctionType: manipula o no raiz, recursando em argtypes e returns.
    - ast.Subscript:    tipo generico (list[int]); recursa no value e no slice.
    - ast.Tuple:        varios tipos (dict[str, int]); recursa em cada elemento.
    - ast.Name:         caso base/folha; aplica o mapa de renomeacao.
    """
    # No FunctionType: caso da raiz -> recursao nos tipos dos args e no retorno.
    # Laco for explicito (sem comprehension) para ser compativel com o recpython.
    if isinstance(no, ast.FunctionType):
        novos_argtypes = []
        for a in no.argtypes:
            novos_argtypes.append(mapeia_tipos(a, mapa))
        return ast.FunctionType(
            argtypes=novos_argtypes,
            returns=mapeia_tipos(no.returns, mapa),
        )

    # Tipo generico parametrizado, ex: list[str] -> recursa no value e no slice
    if isinstance(no, ast.Subscript):
        return ast.Subscript(
            value=mapeia_tipos(no.value, mapa),
            slice=mapeia_tipos(no.slice, mapa),
            ctx=ast.Load(),
        )

    # Tupla de tipos, ex: o slice de dict[str, int] -> recursa em cada elemento
    if isinstance(no, ast.Tuple):
        novos_elts = []
        for e in no.elts:
            novos_elts.append(mapeia_tipos(e, mapa))
        return ast.Tuple(
            elts=novos_elts,
            ctx=ast.Load(),
        )

    # Caso base: nome de tipo (folha) -> troca pelo nome mapeado, se houver
    if isinstance(no, ast.Name):
        return ast.Name(id=mapa.get(no.id, no.id), ctx=ast.Load())

    # Qualquer outro no fica inalterado
    return no


# Entrada do benchmark: tipo generico profundamente aninhado list[list[...[int]]].
# Construido programaticamente porque o parser nao aceita tantos colchetes aninhados.
profundidade = 1_000
arvore_tipo = ast.Name(id="int", ctx=ast.Load())
for _ in range(profundidade):
    arvore_tipo = ast.Subscript(
        value=ast.Name(id="list", ctx=ast.Load()),
        slice=arvore_tipo,
        ctx=ast.Load(),
    )
arvore = ast.FunctionType(argtypes=[arvore_tipo], returns=ast.Name(id="bool", ctx=ast.Load()))
renomeacao = {"int": "Inteiro", "bool": "Booleano"}


# ===== benchmark por TEMPO (gerado por scripts/gerar_benchmark_tempo.py) =====
# Roda a MESMA chamada do timeit original em lotes por ~BENCH_DURACAO segundos
# (variavel de ambiente, padrao 3) e conta quantas execucoes cabem no tempo,
# normalizando para float: execucoes = K * (DURACAO / tempo_real).
import os as _os
import timeit as _timeit

_DURACAO = float(_os.environ.get("BENCH_DURACAO", "3"))
_bench = _timeit.Timer(lambda: mapeia_tipos(arvore, renomeacao))
_ncal, _tcal = _bench.autorange()          # calibra: lote com _tcal >= 0.2s
if _tcal >= _DURACAO:
    _k, _e = _ncal, _tcal                  # 1 lote ja passou de DURACAO: usa ele
else:
    _alvo = max(1, round(_DURACAO / (_tcal / _ncal)))
    _e = _bench.timeit(number=_alvo)       # roda ~DURACAO segundos
    _k = _alvo
_execucoes = _k * (_DURACAO / _e)          # normaliza para exatamente DURACAO
print(f"execucoes em {_DURACAO}s: {_execucoes:.6f} | {_k} chamadas em {_e:.4f}s")
