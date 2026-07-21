"""
Iteracoes do modo classico do benchmark, por funcao-base.

E o parametro que se ajusta na mao: cada funcao precisa de um N que renda um
tempo mensuravel sem demorar demais (fatorial(1000) 1000x e barato; fib_memo
uma vez ja basta). As versoes output_/_nonrec usam o N da base, via base_de().

Funcao-base fora deste dict sai como 'sem_qtd' no relatorio e no CSV.
"""

QTD_EXECUCOES: dict[str, int] = {
    "binary_search": 1000,
    "conta": 1000,
    "count_bits": 100000,
    "count_matches": 1000,
    "countdown": 1000,
    "factorial": 100,
    "fast_pow": 100000,
    "fatorial": 1000,
    "fib_memo": 1,
    "fibonacci": 100,
    "find_first": 1000,
    "first_missing": 1000,
    "flatten": 10000,
    "Hannoi": 1000,
    "identical_strings": 1000,
    "linear_search": 1000,
    "manipula_no_functiontype": 1000,
    "manipula_no_interactive": 1000,
    "manipula_no_typeignore": 1000,
    "mdc": 1,
    "MergeSort": 1000,
    "non_negative_int_contain_digit": 1000,
    "NumSearchTree": 100,
    "potencia_matriz": 1000,
    "quickselect": 1000,
    "remove_keys": 1000,
    "repete": 1000,
    "safe_parse": 1000,
    "soma_trystar": 1000,
    "sum": 1000,
    "sum_nested": 100000,
    "tamanho": 1000,
    "valid_bst": 1000,
    "woodcutter": 100,
}
