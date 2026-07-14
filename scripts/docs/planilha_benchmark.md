# `planilha_benchmark.py` — gerador da planilha de tempos (LEGADO)

> **Status: legado.** Substituído pela FASE 3 do `benchmark.py`, que embute a
> mesma estrutura. Mantido apenas para regerar a planilha a partir de um CSV já
> coletado, sem remedir nada. Candidato a remoção.

## Papel

Gera `arquivos/xlsx/tempos_execucao.xlsx` (aba `Tempos_Execucao`) **do zero**,
lendo os tempos já coletados em `arquivos/csv/benchmark_results.csv` e
extraindo os parâmetros reais dos fontes do benchmark.

Não depende de nenhum xlsx template: a estrutura que antes vinha da aba
`Tempos_Execucao_v4` do `ling_rec.xlsx` está embutida como constantes
(`HEADERS`, `COMPLEXIDADE`, `OBS`).

## Uso

```
python scripts/planilha_benchmark.py
```

Sem parâmetros — caminhos fixos no script.

## Entradas e saídas

| | Caminho |
|---|---|
| Entrada (tempos) | `arquivos/csv/benchmark_results.csv` |
| Entrada (parâmetros) | `recursive_functions/benchmark/*.py` (AST) |
| Saída | `arquivos/xlsx/tempos_execucao.xlsx` |

## Como funciona

1. **Carrega o CSV** para um dicionário `{arquivo: linha}`. Só linhas com
   `status == ok` e `tempo_ms_por_chamada` preenchido contam; ausentes viram
   `-` na planilha.

2. **Monta a aba** com `openpyxl.Workbook()`:
   - coluna A: rótulos das linhas (negrito);
   - colunas B..Z: uma função por coluna, conforme `COLUNA_PARA_BASE`
     (25 funções — o layout histórico da planilha original).

3. **Preenche por coluna:**

   | Linha | Rótulo | Fonte |
   |---|---|---|
   | 1 | Função | `HEADERS` (nome descritivo) |
   | 2 | Tempo_Recursao_Media | CSV: `<base>.py` |
   | 3 | Tempo_Iteracao_Tail_Media | CSV: `output_<base>.py`; `-` se não há versão tail |
   | 4 | Tempo_Iteracao_Media | CSV: `<base>_nonrec.py` |
   | 5 | Sobrecarga_Tail (rec/it_tail) | fórmula `INDEX/MATCH` por rótulo |
   | 6 | Sobrecarga (rec/it_normal) | fórmula `INDEX/MATCH` por rótulo |
   | 7 | Numero_Iteracoes | CSV: `qtd_execucoes` (rec → tail → nonrec, o primeiro disponível) |
   | 8 | Parametros | extração AST do `timeit(lambda: f(args))` do fonte |
   | 9 | Complexidade de resolução | `COMPLEXIDADE` (anotação manual) |
   | 10 | Obs | `OBS` (anotação manual) |

   A métrica de tempo é `tempo_ms_por_chamada` (média por chamada, em ms).

4. **Extração de parâmetros (AST):** localiza o `timeit.timeit(lambda: f(...))`
   no fonte, resolve variáveis de módulo pelos seus valores (substituição
   recursiva) e abrevia inteiros gigantes (`3534...(207dig)`). É a mesma
   técnica documentada em `docs/benchmark.md`.

5. **Estilo:** cabeçalho verde `FF217346` + fonte branca, zebra manual
   `FFF2F2F2` nas linhas pares, altura uniforme 22.5, `freeze_panes="B2"`,
   sem Tabela/ListObject (o banding de tabela mascara preenchimentos e o
   Google Sheets o reaplica na importação).

## Fórmulas de sobrecarga

```
=IFERROR(ROUND(
   INDEX($A:$AA, MATCH("Tempo_Recursao_Media",      $A:$A, 0), COLUMN()) /
   INDEX($A:$AA, MATCH("Tempo_Iteracao_Tail_Media", $A:$A, 0), COLUMN()),
 3), "-")
```

As linhas são localizadas pelo **rótulo** na coluna A (`MATCH`), não por
número fixo — inserir ou reordenar linhas não quebra as fórmulas. `IFERROR`
converte divisões inválidas (tail `-`) em `-`.

## Diferenças para a FASE 3 do `benchmark.py`

Nenhuma estrutural — o código foi absorvido quase literalmente. A única
diferença operacional: este script **lê o CSV do disco**, enquanto a fase 3
recebe os dados em memória da fase 2. Use este quando quiser regenerar apenas
o xlsx sem rodar o benchmark de novo.
