"""
Convencao de nome dos arquivos medidos.

O nome codifica qual versao da funcao o arquivo contem:

    sum.py          versao recursiva original
    output_sum.py   versao tail-recursion -> iteracao
    sum_nonrec.py   versao iterativa gerada pelo recpython3

Tres scripts dependem dessa convencao — benchmark.py agrupa as versoes de cada
funcao, cobertura.py exclui as derivadas do corpus, planilha_tempos.py acha as
tres no CSV — entao ela e definida aqui uma vez so.
"""

EXT_PY = ".py"
PREFIXO_OUTPUT = "output_"
SUFIXO_NONREC = "_nonrec"
