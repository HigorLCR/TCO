# `planilha_tempos.py` — planilha de tempos do benchmark

## Papel

Produtor visual do benchmark: transforma o `benchmark_results.csv` (medições
do modo clássico do `benchmark.py`) na planilha
`arquivos/xlsx/tempos_execucao.xlsx` (aba `Tempos_Execucao`), montada do zero
com `openpyxl.Workbook()` — sem template externo.

Fica no **fim da cadeia** do benchmark: não mede nada — os tempos vêm do CSV.
A única leitura de fonte é a linha `Parametros`, extraída por AST via
`entrada_de` (importada do `benchmark.py`). Se os benchmarks mudaram, rode
`benchmark.py` antes.

## Uso

```
python scripts/planilha_tempos.py
```

Sem parâmetros — caminhos fixos no script.

## Entradas e saídas

| | Caminho |
|---|---|
| Entrada | `arquivos/csv/benchmark_results.csv` (modo clássico do `benchmark.py`) |
| Saída | `arquivos/xlsx/tempos_execucao.xlsx` (aba `Tempos_Execucao`) |

## Estrutura da planilha

Toda a estrutura vem de constantes editáveis no script:

| Constante | Conteúdo |
|---|---|
| `COLUNA_PARA_BASE` | coluna B..Z → stem da função no CSV (25 funções) |
| `HEADERS` | linha 1: **só o nome** da função (sem parâmetros) |
| `COMPLEXIDADE` | linha 9: `O(n)`, `O(log min(a,b))`, ... (anotação manual) |
| `OBS` | linha 10: observações de pesquisa (anotação manual) |

Layout das linhas (rótulo na coluna A):

```
2  Tempo_Recursao_Media        <- <nome>.py          (ms/chamada)
3  Tempo_Iteracao_Tail_Media   <- output_<nome>.py   ('-' se não há versão tail)
4  Tempo_Iteracao_Media        <- <nome>_nonrec.py
5  Sobrecarga_Tail             =  fórmula rec/tail
6  Sobrecarga                  =  fórmula rec/nonrec
7  Numero_Iteracoes            <- qtd_execucoes
8  Parametros                  <- extração AST (entrada_de do benchmark.py)
9  Complexidade de resolução   <- constante
10 Obs                         <- constante
```

## Detalhes

- as fórmulas de sobrecarga (`_formula_sobrecarga`) usam
  `INDEX($A:$AA, MATCH("<rótulo>", $A:$A, 0), COLUMN())` — localizam a linha
  pelo **texto do rótulo**, então inserir/reordenar linhas não as quebra;
  `IFERROR(..., "-")` faz a divisão por `-` (sem tail) virar `-`;
- `_tempo` é o lookup seguro no CSV (`tempo_ms_por_chamada` como float, ou
  `None` → `-` na célula se o arquivo falhou); `_qtd_iter` pega
  `qtd_execucoes` tentando rec → tail → nonrec;
- visual manual: cabeçalho verde `FF217346` + fonte branca, zebra `FFF2F2F2`
  nas linhas pares, altura 22.5, coluna A larga, `freeze_panes="B2"`;
- **sem Tabela/ListObject**: o banding de tabela mascara preenchimentos
  manuais e o Google Sheets o reaplica na importação.

## Decisões de projeto

- **Aba com 25 funções**: `COLUNA_PARA_BASE` herda o layout histórico da
  planilha original; o `benchmark.py` processa todas as 35 funções — apenas o
  xlsx é restrito ao mapa. Para ampliar, estenda os quatro dicionários e a
  faixa `$A:$AA` das fórmulas.
