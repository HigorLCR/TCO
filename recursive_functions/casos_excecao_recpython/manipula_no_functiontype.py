import ast

# Funcao recursiva que manipula um no ast.FunctionType.
# A raiz aqui e um FunctionType (mode="func_type"), que representa um
# "type comment" no formato  (tipos_dos_args) -> tipo_de_retorno.
# Em vez de dobrar constantes (nao ha aritmetica em tipos), a manipulacao
# analoga e renomear recursivamente os nomes de tipo segundo um mapa,
# descendo por tipos genericos aninhados como list[dict[str, int]].
#
# OBS: esta e a versao COM list comprehension. Ela NAO e compativel com o
# transformador recpython3 (a variavel de laco da comprehension tem escopo
# proprio e e perdida na conversao). A versao compativel, com laco for
# explicito, esta em recursive_functions/newfunc/manipula_no_functiontype.py


def mapeia_tipos(no, mapa):
    """Recebe e devolve um no, renomeando recursivamente nomes de tipo.

    - ast.FunctionType: manipula o no raiz, recursando em argtypes e returns.
    - ast.Subscript:    tipo generico (list[int]); recursa no value e no slice.
    - ast.Tuple:        varios tipos (dict[str, int]); recursa em cada elemento.
    - ast.Name:         caso base/folha; aplica o mapa de renomeacao.
    """
    # No FunctionType: caso da raiz -> recursao nos tipos dos args e no retorno
    if isinstance(no, ast.FunctionType):
        return ast.FunctionType(
            argtypes=[mapeia_tipos(a, mapa) for a in no.argtypes],
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
        return ast.Tuple(
            elts=[mapeia_tipos(e, mapa) for e in no.elts],
            ctx=ast.Load(),
        )

    # Caso base: nome de tipo (folha) -> troca pelo nome mapeado, se houver
    if isinstance(no, ast.Name):
        return ast.Name(id=mapa.get(no.id, no.id), ctx=ast.Load())

    # Qualquer outro no fica inalterado
    return no


# Demonstracao: parse em mode="func_type" produz a raiz ast.FunctionType
codigo = "(int, list[str]) -> dict[str, bool]"
arvore = ast.parse(codigo, mode="func_type")
print("Tipo da raiz:", type(arvore).__name__)
print("Antes :", ast.unparse(arvore))

renomeacao = {"int": "Inteiro", "str": "Texto", "bool": "Booleano"}
mapeada = mapeia_tipos(arvore, renomeacao)
ast.fix_missing_locations(mapeada)
print("Depois:", ast.unparse(mapeada))

# A raiz manipulada continua sendo um no FunctionType
print("Raiz ainda e FunctionType?", isinstance(mapeada, ast.FunctionType))
